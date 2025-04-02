cd dev
if [ ! -d tools]; then
  mkdir tools
fi
cd tools
curl -O https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_7_x/ViennaRNA-2.7.0.tar.gz #--file from github doesnt work
tar -zxvf ViennaRNA-2.7.0.tar.gz
cd ViennaRNA-2.7.0
./configure
make
sudo make install