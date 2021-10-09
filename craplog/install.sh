#!/bin/bash

printf "\nWelcome to $(tput setaf 1)C$(tput setaf 3)R$(tput setaf 2)A$(tput setaf 6)P$(tput setaf 4)L$(tput setaf 5)O$(tput setaf 7)G$(tput sgr0)'s installer\n\n"
sleep 1 && wait

printf "This script will ask for $(tput setaf 1)sudo$(tput sgr0) privileges to copy the executable inside $(tput setaf 3)/usr/bin/$(tput sgr0)\nIf you prefer to do it manually, answer [$(tput bold)N$(tput sgr0)] to the incoming question and follow the instructions on screen\n"
printf "CONTINUE? [Y/N] : "
read agree
case "$agree"
	in
		"y" | "Y")
			printf "\n\n"
		;;
		*)
			printf "\nInstallation ABORTED\n\n"
			sleep 1 && wait
			printf "MANUAL INSTALLATION STEPS:\n"
			printf "$(tput bold)1$(tput sgr0)] TAKE NOTE OF THE FULL PATH TO CRAPLOG'S FOLDER\n"
			printf "$(tput bold)2$(tput sgr0)] CREATE A FILE NAMED '$(tput setaf 12)craplog$(tput sgr0)'\n"
			printf "$(tput bold)3$(tput sgr0)] OPEN IT AND WRITE THE FOLLOWING LINES:\n\n$(tput setaf 13)#!/bin/bash\npython3 $(tput setaf 9)/replace/this/with/the/full/path/of/$(tput setaf 13)craplog.py$(tput sgr0)\n\n"
			printf "$(tput bold)4$(tput sgr0)] SAVE AND GIVE EXECUTION PERMISSION IT\n"
			printf "$(tput bold)5$(tput sgr0)] MOVE IT INSIDE '$(tput setaf 12)/usr/bin/$(tput sgr0)'\n"
			printf "$(tput bold)6$(tput sgr0)] GIVE EXECUTION PERMISSION TO EVERY '$(tput setaf 11)*$(tput setaf 2).sh'$(tput sgr0) AND '$(tput setaf 11)*$(tput setaf 2).py$(tput sgr0)' FILE INSIDE CRAPLOG'S MAIN AND SUB FOLDERS\n"
			printf "$(tput bold)7$(tput sgr0)] TRY TO SEE IF IT WORKS\n\n"
			exit
		;;
	esac

# INSTALLATION SECTION
#
# GETTING THE PATH OF CRAPLOG'S FOLDER
crapdir="$(dirname $(realpath $0))"
# CHECKING THE EXISTENCE
if [ -e /usr/bin/craplog ]
	then
		while true;
			do
				printf "\n$(tput setaf 3)WARNING$(tput sgr0): file $(tput setaf 8)/usr/bin/$(tput setaf 1)craplog$(tput sgr0) already exist\n\n"
				printf "IF YOU CHOOSE TO CONTINUE, ACTUAL FILE WILL BE LOST FOREVER\nOverwrite file? [Y/n] : "
				read agree
				case "$agree"
					in
						"Y")
							printf "\n"
							break
						;;
						"y")
							printf "Please answer using capital 'Y'"
						;;
						*)
							printf "Installation ABORTED\n\n"
							exit
						;;
					esac
			done
	fi

# EVERYTHING WENT GOOD
printf "Installing ...\n"

# CREATING EXECUTABLE
printf "#" > ./craplog.tmp
printf "!/bin/bash\n" >> ./craplog.tmp
printf "python3 $crapdir/craplog.py\n\n" >> ./craplog.tmp
# MOVING INSIDE /usr/bin
sudo mv ./craplog.tmp /usr/bin/craplog

# GIVING EXECUTION PERMISSION TO FILE
chmod +x ./craplog.py

# INSTALLING DEPENDENCIES
printf "Do you want to install dependencies? [Y/N] : "
read agree
	case "$agree"
		in
			"Y" | "y")
				printf "\nInstalling Dependencies ...\n"
				for dep in "time" "pathlib" "datetime" "subprocess" "collections"
					do
						pip3 install "$dep"
					done
			;;
			*)
				printf "\n"
			;;
		esac

# FIN
printf "Done\n\n"
sleep 1 && wait
printf "You can now run CRAPLOG simply typing 'craplog' inside your terminal\n\n"
sleep 1 && wait
printf "$(tput setaf 3)F$(tput setaf 2)I$(tput setaf 6)N$(tput sgr0)\n\n"
