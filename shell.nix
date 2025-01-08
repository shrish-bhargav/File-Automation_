let 
	nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11";
	pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
	packages = with pkgs; [
		cowsay
		lolcat
		python312
		python3Packages.watchdog
	];
	GREETING = "Hello, gingerbread!";

	shellHook = ''
		echo $GREETING | cowsay | lolcat
	'';
}
