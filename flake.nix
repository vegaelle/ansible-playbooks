{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-2405";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      ANSIBLE_COLLECTIONS_PATH = ansibleGenerateCollection pkgs.ansible (import ./requirements.nix);
    in
    {
      default = pkgs.mkShell {
        # You could add extra packages you need here too
        packages = [ 
          (pkgs.python312.WithPackages(ps: with ps; [
            ansible passlib bcrypt ansible_vault
          ])
        ]; 
        profile = ''
          ex»port ANSIBLE_COLLECTIONS_PATHS="${ANSIBLE_COLLECTIONS_PATH}"
          export PROXMOX_USERNAME="ansible@pve"
          export PROXMOX_PASSWORD=$(secret-tool lookup name ansible_proxmox_user)
          export PROXMOX_URL="https://hv.ondule.fr:8006"
          export ANSIBLE_VAULT_PASSWORD_FILE=./get-ansible-env
        '';
      };
    };
}

