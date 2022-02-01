mkdir stage
cd stage
git clone https://github.com/micgesham/central_tools.git
cd central_tools
cp -R * ../..
cd ../..
rm -rf stage
