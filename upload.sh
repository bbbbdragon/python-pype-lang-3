sudo rm -rf build dist python_pype_lang_3.egg-info
./reinstall_from_source.sh
twine upload dist/* 
