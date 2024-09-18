import subprocess
import os
from colorama import Fore, Style, init

init(autoreset=True)

common_files = [
    "NTDLL.DLL", "KERNEL32.DLL", "KERNELBASE.DLL", "LOCALE.NLS", "ADVAPI32.DLL", 
    "MSVCRT.DLL", "SECHOST.DLL", "RPCRT4.DLL", "UCRTBASE.DLL", "CRYPT32.DLL", 
    "GDI32.DLL", "WIN32U.DLL", "GDI32FULL.DLL", "MSVCP_WIN.DLL", "USER32.DLL", 
    "D3D11.DLL", "D3DCOMPILER_47.DLL", "IMM32.DLL", "NORMALIZ.DLL", "DXGI.DLL", 
    "WLDAP32.DLL", "WS2_32.DLL", "VCRUNTIME140.DLL", "VCRUNTIME140_1.DLL", 
    "MSVCP140.DLL", "CRYPTBASE.DLL", "BCRYPTPRIMITIVES.DLL", "APPHELP.DLL", 
    "SYSMAIN.SDB"
]

prefetch_dir = "C:\\Windows\\Prefetch"

def parse_prefetch_file(file_path):
    result = subprocess.run(["PECmd.exe", "-f", file_path], capture_output=True, text=True)
    return result.stdout

def extract_info_from_output(output):
    imports = []
    created_on = modified_on = last_accessed_on = None
    capture = False

    for line in output.splitlines():
        if "Created on:" in line:
            created_on = line.split("Created on:")[-1].strip()
        elif "Modified on:" in line:
            modified_on = line.split("Modified on:")[-1].strip()
        elif "Last accessed on:" in line:
            last_accessed_on = line.split("Last accessed on:")[-1].strip()

        if "Files referenced:" in line:
            capture = True
        elif "Directories referenced:" in line:
            capture = False
        elif capture and "\\" in line:
            filename = os.path.basename(line.split("\\")[-1])
            imports.append(filename.upper())

    return imports, created_on, modified_on, last_accessed_on

def main():
    for prefetch_file in os.listdir(prefetch_dir):
        if prefetch_file.endswith(".pf"):  
            file_path = os.path.join(prefetch_dir, prefetch_file)
            output = parse_prefetch_file(file_path)
            imports, created_on, modified_on, last_accessed_on = extract_info_from_output(output)
            
            if all(f in imports for f in common_files):
                print(f"{Fore.MAGENTA}Prefetch File: {prefetch_file}")
                print(f"{Fore.LIGHTMAGENTA_EX}  Created on: {created_on}")
                print(f"{Fore.LIGHTMAGENTA_EX}  Modified on: {modified_on}")
                print(f"{Fore.LIGHTMAGENTA_EX}  Last accessed on: {last_accessed_on}\n")
                print(f"{Fore.MAGENTA}Nitr0 Detected\n")

    input(f"{Fore.MAGENTA}Processing complete. Press Enter to close the script.")

if __name__ == "__main__":
    main()
