{
  description = "Wetterprojekt development environment";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShellNoCC {
        packages = with pkgs; [
          python314
          python314Packages.requests
          python314Packages.tkinter
          python314Packages.matplotlib
          sqlite
        ];
	env = [
	  { name = "p"; value = "python3"; }
	  { name = "sql"; value = "sqlite3"; }
	];
      };
    };
}
