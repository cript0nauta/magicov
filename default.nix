with (import <nixpkgs> { });

let custom-pasta =
  python3.pkgs.google-pasta.overrideAttrs (_: {
    src = fetchFromGitHub {
      owner = "google";
      repo = "pasta";
      rev = "v0.2.0";
      sha256 = "1b2np56sx99092bcg288xi45f55f1rjxg7rjncdy0iynr8zxbcfn";
    };
    doInstallCheck = false;
  });

in python3.pkgs.buildPythonPackage {
  pname = "magicov";
  version = "0.1";
  src = lib.cleanSource ./.;
  doCheck = true;
  propagatedBuildInputs = (with python3.pkgs; [ coverage custom-pasta click ]);
  checkInputs = with python3.pkgs; [ coverage ];
  checkPhase = ''
    python run_tests.py
  '';
}
