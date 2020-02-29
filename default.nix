with (import <nixpkgs> { });

let custom-pasta =
  python3.pkgs.google-pasta.overrideAttrs (_: {
    src = fetchFromGitHub {
      owner = "google";
      repo = "pasta";
      rev = "7c1538c9991badf205214e9f4e567cc4f1879ce6";
      sha256 = "17msrd0irnakznxrcqd3vjf8asz44fl6xlvl47m7la1635nmlbr6";
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
