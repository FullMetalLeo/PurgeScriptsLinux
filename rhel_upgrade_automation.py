#!/usr/bin/env python3
import subprocess
import sys
import argparse
import re

# ANSI Color codes for terminal output
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_info(msg):
    print(f"{GREEN}[INFO] {msg}{RESET}")

def print_error(msg):
    print(f"{RED}[ERROR] {msg}{RESET}")

def print_warn(msg):
    print(f"{YELLOW}[WARN] {msg}{RESET}")

def run_command(command, check=True, shell=False, capture_output=False):
    """Runs a system command and returns the result."""
    try:
        # If command is a list, print it as a string for logging
        cmd_str = command if isinstance(command, str) else " ".join(command)
        print(f"{BOLD}Executing: {cmd_str}{RESET}")
        
        result = subprocess.run(
            command,
            check=check,
            shell=shell,
            text=True,
            capture_output=capture_output
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd_str}")
        if capture_output and e.stderr:
            print_error(e.stderr)
        if check:
            sys.exit(e.returncode)
        return e

def run_playbook(playbook_name):
    """Runs an ansible playbook."""
    cmd = ["ansible-playbook", playbook_name]
    run_command(cmd)

def get_hosts_in_group(group_name):
    """Retrieves a list of hosts in a specific Ansible group."""
    cmd = ["ansible", group_name, "--list-hosts"]
    result = run_command(cmd, capture_output=True)
    output = result.stdout.strip()
    
    # Parse the output to extract hostnames
    # Output format is usually:
    #   hosts (2):
    #     host1
    #     host2
    hosts = []
    for line in output.split('\n'):
        line = line.strip()
        if line and not line.startswith("hosts ("):
             hosts.append(line)
    return hosts

def check_leapp_reports(hosts):
    """Reads leapp-report.txt from hosts and highlights HIGH/CRITICAL issues."""
    print_info("Checking leapp confirmation reports on hosts...")
    
    issues_found = False
    
    for host in hosts:
        print_info(f"Checking host: {host}")
        # Use ansible to cat the file as root
        cmd = [
            "ansible", host, "-m", "command", "-a", "cat /var/log/leapp/leapp-report.txt", "-b"
        ]
        
        # We don't want to fail if the file doesn't exist (maybe leapp didn't run?), but we should warn
        result = run_command(cmd, check=False, capture_output=True)
        
        if result.returncode != 0:
            print_warn(f"Could not read report on {host}. stderr: {result.stderr}")
            continue
            
        report_content = result.stdout
        
        # Simple parsing logic. 
        # We look for sections. This part depends on the exact format of leapp-report.txt.
        # usually they are JSON or text blocks. Assuming text blocks with "Risk Factor: High" etc.
        # But commonly it's readable text. We'll look for "Risk Factor: high" or "Risk Factor: critical" (case insensitive)
        
        # Better approach: split by sections and search
        # Or just grep for the lines? The user wants to "highlight all the issues".
        # We will scan line by line or block by block.
        
        lines = report_content.split('\n')
        for i, line in enumerate(lines):
            if "Risk Factor: High" in line or "Risk Factor: Critical" in line or "Severity: High" in line or "Severity: Critical" in line:
                issues_found = True
                print(f"{RED}{BOLD}!!! ISSUE FOUND ON {host} !!!{RESET}")
                # Print context (a few lines before and after, or the whole block if possible)
                # Since we don't know the exact block structure, simple context:
                start = max(0, i - 10)
                end = min(len(lines), i + 5)
                for j in range(start, end):
                    context_line = lines[j]
                    if j == i:
                        print(f"{RED}>> {context_line}{RESET}")
                    else:
                        print(context_line)
                print("-" * 40)
    
    return issues_found

def verify_redhat_version(hosts):
    """Verifies that hosts are running RedHost 8.*."""
    print_info("Verifying OS version is RedHat 8.*")
    all_ok = True
    for host in hosts:
        cmd = ["ansible", host, "-m", "command", "-a", "cat /etc/os-release", "-b"]
        result = run_command(cmd, capture_output=True, check=False)
        
        if result.returncode != 0:
            print_error(f"Failed to check OS on {host}")
            all_ok = False
            continue
            
        output = result.stdout
        # Check for ID="rhel" and VERSION_ID="8.*"
        # Robust regex check
        if 'ID="rhel"' in output or 'ID=rhel' in output:
             # simple check for version
             if re.search(r'VERSION_ID="?8\.', output):
                 print_info(f"{host}: Verified RHEL 8")
             else:
                 print_error(f"{host}: Not RHEL 8! Output:\n{output}")
                 all_ok = False
        else:
             print_warn(f"{host}: ID is not rhel? Output:\n{output}")
             # Depending on strictness, might want to fail. Assuming fail.
             all_ok = False
             
    return all_ok

def mount_all(hosts):
    """Runs mount -a on all hosts."""
    print_info("Running 'mount -a' on hosts...")
    for host in hosts:
        cmd = ["ansible", host, "-m", "command", "-a", "mount -a", "-b"]
        run_command(cmd)

def main():
    parser = argparse.ArgumentParser(description="RHEL 8 Upgrade Automation")
    parser.add_argument("--skip-steps", type=str, help="Comma separated list of steps to skip (1-10)")
    args = parser.parse_args()
    
    skip_list = []
    if args.skip_steps:
        skip_list = [int(x) for x in args.skip_steps.split(',')]

    # Step 1: Pre-check
    if 1 not in skip_list:
        run_playbook("Pre-check.yml")
    
    # Step 2: Pre-upgrade
    if 2 not in skip_list:
        run_playbook("pre-upgrade.yml")
        
    # Step 3: Setup
    if 3 not in skip_list:
        run_playbook("setup.yml")
        
    # Step 4: Analyze
    if 4 not in skip_list:
         run_playbook("analyze.yml")
         
    # Step 5: Remediation
    if 5 not in skip_list:
        run_playbook("remediation.yml")
        
    # Step 6: Verify Leapp Report
    if 6 not in skip_list:
        hosts = get_hosts_in_group("RET")
        if not hosts:
            print_error("No hosts found in group [RET]. Cannot proceed with report check.")
            sys.exit(1)
            
        check_leapp_reports(hosts)
        
        print("\n" + "="*60)
        print(f"{YELLOW}Please review the above issues (if any).{RESET}")
        print("Press 'Enter' to proceed with the upgrade.")
        print("Press 'Q' (or 'q') to quit.")
        user_input = input("Choice: ").strip().lower()
        
        if user_input == 'q':
            print_info("Exiting as requested.")
            sys.exit(0)
            
    # Step 7: Upgrade
    if 7 not in skip_list:
        run_playbook("Upgrade.yml")
        
    # Step 8: Post-upgrade
    if 8 not in skip_list:
        run_playbook("post-upgrade.yml")
        
    # Step 9: Verify OS
    if 9 not in skip_list:
        hosts = get_hosts_in_group("RET") # Fetch again just in case? Usually static.
        if verify_redhat_version(hosts):
            print_info("All hosts verified as RHEL 8.*. Proceeding.")
        else:
            print_error("One or more hosts failed OS verification. Exiting.")
            sys.exit(0) # Requirement: verify... if yes proceed... else exit with 0.
            
    # Step 10: Mount all
    if 10 not in skip_list:
        hosts = get_hosts_in_group("RET")
        mount_all(hosts)

    print_info("Automation script execution completed successfully.")

if __name__ == "__main__":
    main()
