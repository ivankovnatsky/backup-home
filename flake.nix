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

            # Runtime dependencies with version constraints
            propagatedBuildInputs = with pkgs; [
              (rclone.overrideAttrs (old: {
                meta = old.meta // {
                  minVersion = "1.50.0";  # Minimum required version
                };
              }))
              (if stdenv.isDarwin then 
                (pigz.overrideAttrs (old: {
                  meta = old.meta // {
                    minVersion = "2.4";  # Minimum required version
                  };
                }))
              else 
                (gzip.overrideAttrs (old: {
                  meta = old.meta // {
                    minVersion = "1.10";  # Minimum required version for gzip
                  };
                })))
              (if !stdenv.isDarwin then 
                (gnutar.overrideAttrs (old: {
                  meta = old.meta // {
                    minVersion = "1.34";  # Minimum required version for tar
                  };
                }))
              else null)
            ];

            # Add post-installation check
            postInstall = ''
              $out/bin/backup-home --help > /dev/null
            '';
          };
          default = self.packages.${system}.backup-home;
        };

        # Development shell with all tools
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            poetry
            rclone
            pigz
            ruff
          ];

          # Add shell hook to verify environment
          shellHook = ''
            echo "Checking development environment..."
            command -v rclone >/dev/null 2>&1 || { echo "rclone is required but not installed."; exit 1; }
            command -v pigz >/dev/null 2>&1 || { echo "pigz is required but not installed."; exit 1; }
            command -v poetry >/dev/null 2>&1 || { echo "poetry is required but not installed."; exit 1; }
            echo "Development environment is ready!"
          '';
        };

        # Add checks
        checks.${system} = {
          build-test = self.packages.${system}.backup-home;
        };
      });
} 
