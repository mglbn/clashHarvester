mkdir -p ~/.config/systemd/user
cp ./clashHarvester.service ~/.config/systemd/user/ 
systemctl --user enable clashHarvester
loginctl enable-linger $USER