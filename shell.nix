
with (import <nixpkgs> {});
mkShell {
  buildInputs = (with python27Packages;
    [virtualenv ipython coverage
    ]);
  shellHook = ''
      unset SOURCE_DATE_EPOCH  # Required to make pip work
      VENV_PATH=.venv

      mkvirtualenv(){
        # Reset previous virtualenv
        type -t deactivate && deactivate
        rm -rf $VENV_PATH

        # Build new virtualenv with system packages
        virtualenv --system-site-packages $VENV_PATH
        source $VENV_PATH/bin/activate
        pip install -e git+https://github.com/google/pasta#egg=pasta
      }

      if [[ -d $VENV_PATH ]]; then
        source $VENV_PATH/bin/activate
      else
        echo Creating new virtualenv
        mkvirtualenv
      fi
  '';
}

