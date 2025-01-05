{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/8a36010652b4571ee6dc9125cec2eaebc30e9400";
    flake-utils.url = "github:numtide/flake-utils/11707dc2f618dd54ca8739b309ec4fc024de578b";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in
      {
        packages = {
          backup-home = mkPoetryApplication {
            projectDir = ./.;
            preferWheels = true;

            # Runtime dependencies
            propagatedBuildInputs = with pkgs; [
              rclone
              pigz
              p7zip
            ];
          };
          default = self.packages.${system}.backup-home;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            poetry
            rclone
            pigz
            p7zip
            ruff
          ];
        };
      });
} 
