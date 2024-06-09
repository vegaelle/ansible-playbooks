{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  inputs.ansible2nix.url = "github:teto/ansible2nix";

  outputs = { self, nixpkgs, ansible2nix }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      ansible2nixPackage = import ansible2nix;
      ANSIBLE_COLLECTIONS_PATH = ansible2nixPackage.ansibleGenerateCollection pkgs.ansible (import ./requirements.nix);
    in
    {
      devShell.x86_64-linux = pkgs.mkShell {
        # You could add extra packages you need here too
        packages = [ 
          (pkgs.python312.withPackages(ps: with ps; [
            ansible passlib bcrypt ansible-vault-rw
          ]))
        ]; 
        shellHook = ''
          export ANSIBLE_COLLECTIONS_PATHS="${ANSIBLE_COLLECTIONS_PATH}"
          export PROXMOX_USERNAME="ansible@pve"
          export PROXMOX_PASSWORD=$(secret-tool lookup name ansible_proxmox_user)
          export PROXMOX_URL="https://hv.ondule.fr:8006"
          export ANSIBLE_VAULT_PASSWORD_FILE=./get-ansible-env
        '';
      };
    };
}

