#!/bin/bash
# Makes the bash script to print out every command before it is executed except echo
#trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG


########################## INITIALISATION ################################
if [[ -d "$HOME/Android" ]];then
  ANDROID_FOLDER="$HOME/Android"
else
  mkdir "$HOME/Android"
  ANDROID_FOLDER="$HOME/Android"
fi



function SayFinalMessage (){
  say -v Victoria Everything have been installed successfully! You can now automate your smartphone. Please read carefully the popup message.
}
#function DisplayPopup (){
#
#  osascript <<'END'
#      set theAlertText to "How to enable USB DEBUG?"
#      set theAlertMessage to "\nAll necessary software has been installed successfully. Your computer is able now to automate smartphones through a USB cable.\n- 1 You need to enable 'Developer options' on your Android smartphone.\n\n- 2 Then you will be able to enable USB Debugging \n\n- 3 Finally, you will plug your smartphone into your computer with a USB cable.\n\nAfter steps 1,2, and 3 are done, PhoneBot has the 'Scan Smartphones' button in the tab 'Settings' to help you to recognize your smartphone.\n\nWould you like to know how to enable 'Developer options'??"
#      display alert theAlertText message theAlertMessage as critical buttons {"Cancel", "Watch Video"} default button "Watch Video" cancel button "Cancel" giving up after 60
#      set the button_pressed to the button returned of the result
#      if the button_pressed is "Watch Video" then
#          open location "https://www.youtube.com/watch?v=VcbDvsveqEs?t=19&hl=en&cc_lang_pref=en&cc=1"
#      end if
#  END
#
#
#}



#########################################################################################################
#                FUNCTION TO REMOVE DUPLICATES FROM A LINE
#########################################################################################################

function RemoveDuplicateFromLine() {
  # Remove the duplicate
  myvariable=$(echo "$1" | tr ':' '\n' | sort | uniq | xargs)
  #echo "### myvariable : $myvariable"
  # Replace the spaces by :
  result=${myvariable// /:}
  echo "$result"

}


#########################################################################################################
#                FUNCTION TO ADD VALUE $2 IN ENV VAR
#########################################################################################################

function ExportPATH(){
  echo "========================= ExportPATH =========================="
  echo "========================= $1 $2 =========================="
  echo "==============================================================="

  if [[ $1 = "PATH" ]] ;then
    echo "PATH BEFORE : $PATH"
    PATH_VALUE=$PATH

    #echo "PATH_VALUE : $PATH_VALUE"
    if [[ -z $PATH_VALUE ]];then
      NEW_PATH_VALUE=$2
    else
      NEW_PATH_VALUE=$PATH_VALUE:$2
    fi
    #echo "NEW_PATH_VALUE is $NEW_PATH_VALUE"
    if [[ $NEW_PATH_VALUE = *":"* ]] ;then
      NEW_PATH_VALUE=$(RemoveDuplicateFromLine $NEW_PATH_VALUE)
    fi
    echo "PATH AFTER : $PATH"
    export PATH=$NEW_PATH_VALUE
  fi


  if [[ $1 = "ANDROID_HOME" ]] ;then
    ANDROID_HOME_VALUE=$ANDROID_FOLDER

    export ANDROID_HOME="$ANDROID_FOLDER"
  fi


  if [[ $1 = "JAVA_HOME" ]];then
    JAVA_HOME_VALUE=$JAVA_HOME
    #echo "JAVA_HOME_VALUE : $JAVA_HOME_VALUE"
    if [[ -z $JAVA_HOME_VALUE ]];then
      NEW_JAVA_HOME_VALUE=$2
    else
      NEW_JAVA_HOME_VALUE=$2
    fi
    #echo "NEW_JAVA_HOME_VALUE is $NEW_JAVA_HOME_VALUE"
    if [[ $NEW_JAVA_HOME_VALUE = *":"* ]] ;then
      NEW_JAVA_HOME_VALUE=$(RemoveDuplicateFromLine $NEW_JAVA_HOME_VALUE)
    fi
    export JAVA_HOME="$NEW_JAVA_HOME_VALUE"
  fi
}



#########################################################################################################
#                FUNCTION TO EDIT OR ADD THE INSTALLATION VARIABLES IN CONFIG.INI FILE
#########################################################################################################


function ChangeConfigIni() {
   echo "=========================== ChangeConfigIni ==================================="
   #echo "Variables are $1 (name of variable) and $2 (value of variable)"

   #FUNCTION TO CHANGE OR ADD VALUES OF INSTALLATION VARIABLES:
   #APPIUM,NODE,ANDROID,BUILD_TOOLS,TESSERACT,JAVA
   #THE FILES
   #echo $HOME
   CONFIG_INI_FILE_FILENAME="config.ini"
   CONFIG_INI_FILE="$HOME/PhoneBot/$CONFIG_INI_FILE_FILENAME"

   if [ ! -f "$CONFIG_INI_FILE" ]
   then
      echo "Setting up config file..."
      echo "[Settings]" >> "$CONFIG_INI_FILE"
   fi

   #HERE BELOW IS THE NEW LINE WHICH NEED TO BE ADDED OR REPLACED
   NEW_LINE="$1 = $2"



   #THE STRINGS WHICH HELP US TO IDENTIFY EXISTING LINE OF PATH
   APPIUM_STRING="appium ="
   NODE_STRING="node ="
   ANDROID_STRING="android ="
   BUILD_TOOLS_STRING="build_tools ="
   TESSERACT_STRING="tesseract ="
   JAVA_STRING="java ="
   SDKMANAGER_STRING="sdkmanager ="

   #INITIALISATION OF VARIABLES
   APPIUM_EXIST_IN_FILE=0
   NODE_EXIST_IN_FILE=0
   JAVA_EXIST_IN_FILE=0
   BUILD_TOOLS_EXIST_IN_FILE=0
   SDKMANAGER_EXIST_IN_FILE=0
   TESSERACT_EXIST_IN_FILE=0
   ANDROID_EXIST_IN_FILE=0

   VARIABLE_EXIST_IN_FILE=0

   # We need to compare strings with insensitive case
   # https://stackoverflow.com/a/14138301/10551444
   local orig_nocasematch=$(shopt -p nocasematch)
   shopt -s nocasematch
   #LET'S READ ALL THE LINES OF THE FILES AND CHECK IF A VARIABLE $1 EXISTS OR NOT
   while read LINE; do
      #echo "$LINE"
      if [[ $LINE == "$1="* ]] || [[ $LINE == "$1 = "* ]] || [[ $LINE == "$1 ="* ]] || [[ $LINE == "$1= "* ]] ;then
         echo "$1 ALREADY EXIST IN config.ini"
         VARIABLE_EXIST_IN_FILE=1
         LINE_TO_BE_CHANGE=$LINE

      fi
   done < "$CONFIG_INI_FILE"


   #NOW WE KNOW THE LINE WHICH NEED TO BE CHANGE, WE REPLACE IT WITH THE NEW LINE

   #IF THE VARIABLE LINE ALREADY EXIST WE CHANGE IT
   if [[ "$VARIABLE_EXIST_IN_FILE" = 1 ]];then
      echo "Variable $1 is already in file config.ini."
      if [[ "$LINE_TO_BE_CHANGE" == *"$2"* ]]; then
         echo "The value $2 is already in variable $1."
         echo " Have a look at it here below:"
         echo "$LINE_TO_BE_CHANGE"
      else
         #WE CHANGE THE NEW LINE
         echo "WE CHANGE THE NEW LINE"
         sed -i '' "s+${LINE_TO_BE_CHANGE}+${NEW_LINE}+" $CONFIG_INI_FILE
      fi
   else
   #IF THE VARIABLE LINE DOESN'T EXIST, WE ADD IT
      echo "THE VARIABLE LINE DOESN'T EXIST, WE ADD IT"
      echo -e "\n" >> $CONFIG_INI_FILE
      echo "$NEW_LINE" >> $CONFIG_INI_FILE
      echo "[SAVING...]NEW_LINE ADDED IN CONFIG.INI FILE"
   fi

}
#########################################################################################################
#                FUNCTION TO EDIT OR ADD THE ENVI VARIABLES IN THE PROFILE ENV VARIABLE FILE
#########################################################################################################

function UpDateProfileFile (){
  echo "##########################################################################################"
  echo "============================== UpDateProfileFile ========================================="
  echo "============================== $1 $2 $3 ========================================="
  echo "##########################################################################################"



  # WE TEST IF $2 IS NOT EMPTY
  if [[ ! -z "$2" ]];then
    # LET REMOVE THE / FROM $2
    TMP2=$2
    LEN_2=${#TMP2}
    #echo "LEND_2 : $LEN_2"
    LAST_CHAR_2="${TMP2:$LEN_2-1:1}"
    #echo "LAST_CHAR_2 : $LAST_CHAR_2"
    if [[ $LAST_CHAR_2 = "/" ]];then
      TMP2=${TMP2:0:$LEN_2-1}

      #echo "NEW 2 is $TMP2"
    fi



    #FUNCTION TO CHANGE OR ADD PATH ENVIRONMENT VARIABLE IN FILE .zshrc or .bash_profile
    ####################################################################################
    #              WE PREPARE ENVIRONMENT FILE
    ####################################################################################
    #THE FILES
    ZSHRC="$HOME"/.zshrc
    BASH_PROFILE="$HOME"/.bash_profile


    #echo "WE SELECT THE APPROPRIATE ENV FILE DEPENDING ON OS"
    if [[ "$3" == "Catalina" ]];then
        #CHECK IF FILE EXISTS
        if [[ ! -f "$ZSHRC" ]]; then
            touch $ZSHRC
        fi
        ENV_FILE=$ZSHRC
    else
        #CHECK IF FILE EXISTS
        if [[ ! -f "$BASH_PROFILE" ]]; then
            touch $BASH_PROFILE
        fi
        ENV_FILE=$BASH_PROFILE
    fi
    # THERE ARE SEVERAL SCENARIOS SO SEVERAL POSSIBILITIES FOR $1 AND $TMP2
    # If file is empty => STATUS="empty_file"
    # else if $1 is not in file => STATUS="no_1_here"
    # else if $1 is here but not $TMP2 => STATUS="yes_1_no_2"
    # else if $1 and $TMP2 are here => STATUS="yes_1_yes_2"


    # 1RST WE NEED TO CHECK IF PROFILE FILE IS EMPTY OR NOT
    NUMBER_LINES=$(< $ENV_FILE wc -l)
    if [[ -z $NUMBER_LINES ]];then
      NUMBER_LINES=0
    fi
    #echo "NUMBER_LINES : $NUMBER_LINES"
    if [[ "$NUMBER_LINES" -eq 0 ]];then
      STATUS="empty_file"
      #echo "The file is empty"

    fi




    # WE WILL BUILD A TEMP FILE
    temp_file=$(mktemp)
    #temp_file="$HOME/PhoneBot/tmp.tmp"
    #rm $temp_file
    #touch temp_file



    # 2ND WE NEED TO LOOP ENV FILE IN ORDER TO FIND STATUS OF $1 AND $TMP2
    # SO WE WILL LOOP THE FILE AND CHECK EACH LINE


    #!!!!! THE FIRST THING WE NEED TO CHECK IS TO SEE IF LINE IS ABOUT OUR BUSINESS
    # THAT MEANS IF LINE HAS =" ..... AND FINISH BY "
    counter_UpDateProfileFile=1
    while read LINE; do
      #echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
      #echo ">>>>>>>>>>>>>>>>>>>>>>>>>>> CAT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

      #cat $temp_file

      #echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
      #echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

      echo "-------- LINE N° $counter_UpDateProfileFile -----------"
      echo "LINE N°$counter_UpDateProfileFile : $LINE"
      #echo $LINE
      LEN_LINE=${#LINE}
      #echo "LEN_LINE : $LEN_LINE"
      if [[ $LEN_LINE > 0 ]];then
        LAST_CHAR_LINE="${LINE:$LEN_LINE-1:1}"
        #echo "LAST_CHAR_LINE : $LAST_CHAR_LINE"

        if [[ $LINE == *"="* ]]  ;then
          #echo "IT IS INTERESTING LINE FOR US"
          if [[ $LINE == *$1* ]] && [[ $LINE == *$TMP2* ]] ;then

              # THERE ARE $1 AND $TMP2 IN PROFILE FILE. SO WE DO NOT NEED TO DO ANYTHING!"
              STATUS="yes_1_yes_2"
              #echo "STATUS : $STATUS"
              NEW_FRESH_LINE=$LINE
          else
            if [[ $LINE == *$1=* ]] || [[ $LINE == *"$1 ="* ]] ;then
              # HERE WE NEED TO ADD THE VALUE $TMP2 IN THE $LINE
              STATUS="$1 yes_1_no_2"
              #echo "STATUS : $STATUS"
              #echo "BEFORE $TMP2"
              ####################################################
              ####################################################
              ############# HERE IS COMPLICATE ###################
              ####################################################
              ####################################################
              # AS WE NEED TO ADD A VALUE IN EXISTING VARIABLE, WE
              # NEED TO VERIFY THAT  PREVIOUS LAST CHARACTER IS NOT FINISHING BY ":"
              PREVIOUS_LAST_CHAR="${LINE:$LEN_LINE-2:1}"
              #echo "PREVIOUS_LAST_CHAR : $PREVIOUS_LAST_CHAR"
              if [ "$1" = "ANDROID_HOME" ] || [ "$1" = "JAVA_HOME" ];then
                NEW_FRESH_LINE="export $1=\"$2\""
              else
                if [ "$PREVIOUS_LAST_CHAR" = ":" ] || [ "$PREVIOUS_LAST_CHAR" = "\"" ];then
                  #echo "ALERT !!! THERE IS :$LAST_CHAR_LINE or \""
                  PART_1="${LINE:0:$LEN_LINE-2}"
                  NEW_FRESH_LINE="$PART_1:$TMP2$LAST_CHAR_LINE"
                else
                  PART_1="${LINE:0:$LEN_LINE-1}"
                  NEW_FRESH_LINE="$PART_1:$TMP2$LAST_CHAR_LINE"

                  #NO : AS PREVIOUS LAST CHARACTER OF THE LINE
                fi
              fi


              #echo "AFTER $NEW_FRESH_LINE"

            else
              # THERE ARE NOT $1 . SO WE NEED TO DO CREATE ENV VAR!"
              STATUS="no_1_here"
              #echo "STATUS : $STATUS"
              echo $LINE >> $temp_file
              echo "[SAVING...]LINE ADDED IN TEMP FILE"
            fi
          fi
        else
          #echo "NOT INTERESTING LINE. WE COPY PASTE"
          STATUS="just_copy_paste"
          NEW_FRESH_LINE=$LINE
        fi

        if [[ $STATUS != "no_1_here" ]];then
          echo $NEW_FRESH_LINE >> $temp_file
          echo "[SAVING...]NEW_FRESH_LINE ADDED IN TEMP FILE"
        fi
      fi
      echo "--------------------------------------------------"
      echo "--------------------------------------------------"
      echo "--------------------------------------------------"
      echo "--------------------------------------------------"
      ((counter_UpDateProfileFile++))


    done < "$ENV_FILE"
    # IF AT THE END OF THE LOOP, WE NEED TO CREATE EN, WE DO IT.
    # BECAUSE IF WE DO IT IN THE LOOP, IT WILL CREATE ISSUES...
    #echo " "
    #echo "SOULD WE ADD A NEW VARIABLE?"
    #echo " "
    if (grep "$1=" $temp_file) || (grep "$1 =" $temp_file);then
        echo "NO NEED TO CREATE NEW ENV VAR"

    else
      echo "WE DID NOT FIND 1. WE NEED TO CREATE AND ADD A NEW ENV VAR"
      NEW_FRESH_LINE="export $1=\"$TMP2\""
      echo $NEW_FRESH_LINE >> $temp_file
      echo "[SAVING...]NEW_FRESH_LINE ADDED IN TEMP FILE"

    fi

  fi


  echo "+++++++++++++++++++++++++++++"
  #cat $temp_file

  echo "--------------------------------------------------"

  # WE REPLACE THE PROFILE FILE BY THE TEMP FILE
  cp $temp_file $ENV_FILE
  cp $temp_file "$HOME/.zshenv"

  # WE REMOVE TEMP FILE
  rm ${temp_file}

}
#########################################################################################################
#                    FUNCTION TO REMOVE SPACES ON THE LEFT
#########################################################################################################
trim() {
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[[![[:space:]]*}"}"
    printf '%s' "$var"
}

#########################################################################################################
#                    FUNCTION TO REMOVE SPACES ON THE LEFT
#########################################################################################################
GetCorrectSdkmanager() {
    echo "#### WE SEARCH FOR THE PATH OF sdkmanager file ====================================================="

    SDKMANAGER_FILES=$(find "$ANDROID_FOLDER" -name sdkmanager)

    for SDKMANAGER_FILE in $SDKMANAGER_FILES
        do

            #WE PREPARE THE STRING PATH =========================================================================
            WORDTOREMOVE="/sdkmanager"
            SDKMANAGER_FOLDER_TO_ADD=${SDKMANAGER_FILE//$WORDTOREMOVE/}
            #echo "SDKMANAGER_FOLDER_TO_ADD : $SDKMANAGER_FOLDER_TO_ADD"
            if [[ "$SDKMANAGER_FOLDER_TO_ADD" != "$HOME/Android/tools/bin" ]];then
                #WE MAKE THE FOLDER AND FILES EXECUTABLE ==============================================================
                chmod 755 "$SDKMANAGER_FOLDER_TO_ADD"
                chmod 755 "$SDKMANAGER_FOLDER_TO_ADD"/*
                GOOD_SDKMANAGER="$SDKMANAGER_FOLDER_TO_ADD/sdkmanager"
                #echo "EXPORT PATH OF SDKMANAGER ********************************"
                ExportPATH "PATH" "$SDKMANAGER_FOLDER_TO_ADD"
                UpDateProfileFile "PATH" "$SDKMANAGER_FOLDER_TO_ADD" "$MAC_OS_VERSION"

            else
                rm $SDKMANAGER_FILE
                #echo "$SDKMANAGER_FILE has been removed as it was creating issues with java!"
            fi

        done


}
# =============================================================================================================
# =============================================================================================================
# ===================================== HERE START THE SCRIPT =================================================
# =============================================================================================================
# =============================================================================================================



echo "##########################################################################################################"
echo "#                        GET ACTUAL USERNAME           "
echo "##########################################################################################################"
LIST_USERS=$(dscl . list /Users | grep -v '_')
for USER_FROM_LIST in $LIST_USERS
do
    echo "$USER_FROM_LIST"
    if [[ $USER_FROM_LIST != "daemon" ]]; then
        if [[ $USER_FROM_LIST != "nobody" ]]; then
            if [[ $USER_FROM_LIST != "root" ]]; then
                ACTUAL_USER=$USER_FROM_LIST
            fi
        fi
    fi
done


echo "#########################################################################################################"
echo "#                        DETECT MAC OS VERSION"
echo "#########################################################################################################"
os_ver=$(sw_vers -productVersion)
if [[ "$os_ver" == 10.13.* ]]; then
    echo "macOS High Sierra"
    MAC_OS_VERSION="High Sierra"
    BASH_PROFILE_FILE="$HOME/.bash_profile"
elif [[ "$os_ver" == 10.12.* ]]; then
    echo "macOS Sierra"
    MAC_OS_VERSION="Sierra"
    BASH_PROFILE_FILE="$HOME/.bash_profile"
elif [[ "$os_ver" == 10.15.* ]]; then
    echo "macOS Catalina"
    MAC_OS_VERSION="Catalina"
    BASH_PROFILE_FILE="$HOME/.zshrc"
elif [[ "$os_ver" == 10.14.* ]]; then
    echo "macOS Mojave"
    MAC_OS_VERSION="Mojave"
    BASH_PROFILE_FILE="$HOME/.bash_profile"
else
    echo "(Mac) OS X something"
    MAC_OS_VERSION="Else"
    BASH_PROFILE_FILE="$HOME/.bash_profile"
fi

echo "#########################################################################################################"
echo "#                        INITIALISATION PROFILE FILE"
echo "#########################################################################################################"

# !!!!!!!!!!!! FIRST WE TEST IF PATH IS IN CONFIG FILE
if (grep -Fxq "PATH=" $BASH_PROFILE_FILE) || (grep -Fxq "PATH =" $BASH_PROFILE_FILE);then
    # code if found
    echo "Variable PATH is in BASH_PROFILE_FILE"
    # /usr/local/bin is a very important folder to be sure it is in profile file and load it
    UpDateProfileFile "PATH" "/usr/local/bin" "$MAC_OS_VERSION"
    UpDateProfileFile "PATH" "/usr/bin" "$MAC_OS_VERSION"
    UpDateProfileFile "PATH" "/sbin" "$MAC_OS_VERSION"
    UpDateProfileFile "PATH" "/opt/local/bin" "$MAC_OS_VERSION"
    ExportPATH "PATH" "/usr/local/bin"
    ExportPATH "PATH" "/usr/bin"
    ExportPATH "PATH" "/sbin"
    ExportPATH "PATH" "/opt/local/bin"
else
    # code if not found
    echo "export PATH=\"/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/local/bin\"" >> $BASH_PROFILE_FILE
    echo "[SAVING...] basic folders in BASH_PROFILE_FILE"
fi

# WE KNOW THAT ANDROID_HOME FOLDER HAS BEEN CREATED AND WILL NOT CHANGE
UpDateProfileFile "ANDROID_HOME" "$ANDROID_FOLDER" "$MAC_OS_VERSION"




# WE WILL RUN THE SCRIPT 2 TIMES BECAUSE OF ENVIRONMENT VARIABLES WHICH NEED TO BE EFFECTIVE
counter=1
PATH_VALUE=$PATH
while [[ $counter -le 2 ]]
  do


    # Replace a string by a string in a file
    # Here below we remove the double :: and "" from profile file
    sed -i '' 's/\:\:/\:/g' $BASH_PROFILE_FILE
    sed -i '' 's/\"\"/\"/g' $BASH_PROFILE_FILE


    echo "#########################################################################################################"
    echo "#                        REBOOT OR NOT?"
    echo "#########################################################################################################"
    INSTALL_BLOCKED=0
    #Before we start any installation, we need to check if a previous installation is blocked or not
    if [[ -f "/private/var/db/mds/system/mds.install.lock" ]]; then
        echo "A previous installation was blocked. You need to restart the computer!"
        sudo rm /private/var/db/mds/system/mds.install.lock
        INSTALL_BLOCKED=1
    fi


    if [[ -f "//private/var/db/mds/system/mds.lock" ]]; then
        sudo rm /private/var/db/mds/system/mds.lock
        INSTALL_BLOCKED=1
    fi

    if [[ $INSTALL_BLOCKED == 1 ]];then
        #we don't need to reboot with:
        sudo killall -1 installd
        #Reboot
        #COMMAND_TO_BE_ADDED_FOR_REBOOT="sudo /bin/bash $HOME/Dropbox/cff/Python/PhoneBot_0002_FINAL/PhoneBot_Install.sh"
        echo "$COMMAND_TO_BE_ADDED_FOR_REBOOT">> "$BASH_PROFILE_FILE"
        echo "[SAVING...]COMMAND_TO_BE_ADDED_FOR_REBOOT  IN BASH_PROFILE_FILE"
        #/sbin/reboot
    else
        sed -i '' "s+${COMMAND_TO_BE_ADDED_FOR_REBOOT}++" "$BASH_PROFILE_FILE"

    fi


#    echo "#########################################################################################################"
#    echo "#                       CHECK ENVIRONMENT VARIABLE"
#    echo "#########################################################################################################"
#    UpDateProfileFile "PATH" "$PATH" "$MAC_OS_VERSION"
#    UpDateProfileFile "JAVA_HOME" "$JAVA_HOME" "$MAC_OS_VERSION"
#    UpDateProfileFile "ANDROID_HOME" "$ANDROID_HOME" "$MAC_OS_VERSION"


    echo "#########################################################################################################"
    echo "#                            HOMEBREW"
    echo "#########################################################################################################"
    #CHECK BREW ===============================================================================================
    OUTPUT=$(brew --version 2>&1)
    echo "OUTPUT is $OUTPUT"
    if echo "$OUTPUT" | grep -q "command not found"; then
        echo "Brew is NOT installed"
        BREW_INSTALLED=0
    else
        echo "Brew is installed"
        BREW_INSTALLED=1
    fi

    # WE INSTALL BREW IF NECESSARY =============================================================================
    if [[ $BREW_INSTALLED == 0 ]]; then
        say Installation of home brew
        echo "We will install brew"
        /bin/bash -c "$(curl -fsSL https://phonebot.co/dist/Install_Homebrew.sh)"


    fi

    HOMEBREW_FOLDER=$HOME/Library/Caches/Homebrew
    GIT_ATTRIBUTES_FOLDER=$HOME/.config/git/attributes
    if [[ ! -d "$HOMEBREW_FOLDER" ]]; then
        mkdir "$HOMEBREW_FOLDER"
    fi
    #=============
    #sudo chown -R $ACTUAL_USER $GIT_ATTRIBUTES_FOLDER
    #chmod u+w $GIT_ATTRIBUTES_FOLDER
    #============
    sudo chown -R "$ACTUAL_USER" "$HOMEBREW_FOLDER"
    chmod u+w "$HOMEBREW_FOLDER"


    echo "#########################################################################################################"
    echo "#                            MACPORT"
    echo "#########################################################################################################"
    #CHECK BREW ===============================================================================================
    if type port &>/dev/null; then
        echo "MacPort is installed"
        MACPORT_INSTALLED=1
    else
        echo "MacPort is NOT installed"
        MACPORT_INSTALLED=0
    fi

    # WE INSTALL BREW IF NECESSARY =============================================================================
    if [[ $MACPORT_INSTALLED == 0 ]]; then
        say Installation of Mac port
        echo "We will install MacPort"
        #curl -O https://distfiles.macports.org/MacPorts/MacPorts-2.6.3.tar.bz2
        #tar xf MacPorts-2.6.3.tar.bz2
        #MacPorts-2.6.3/./configure
        #MacPorts-2.6.3/make
        #MacPorts-2.6.3/make install
        if [[ "$MAC_OS_VERSION" == "Catalina" ]];then
            FILE_MACPORT="MacPorts-2.7.1-10.15-Catalina.pkg"
        elif [[ "$MAC_OS_VERSION" == "Sierra" ]];then
            FILE_MACPORT="MacPorts-2.7.1-10.12-Sierra.pkg"
        elif [[ "$MAC_OS_VERSION" == "High Sierra" ]];then
            FILE_MACPORT="MacPorts-2.7.1-10.13-HighSierra.pkg"
        elif [[ "$MAC_OS_VERSION" == "Mojave" ]];then
            FILE_MACPORT="MacPorts-2.7.1-10.14-Mojave.pkg"
        fi

        if [[ ! -f "$FILE_MACPORT" ]]; then
            echo "Macport file is not present! We download it."
            #curl -O "https://phonebot.co/dist/$FILE_MACPORT"
            curl -O "https://distfiles.macports.org/MacPorts/$FILE_MACPORT"
        else
            echo "MacPort file is present. We don't need to download it and we will install MacPort now!"
        fi
        installer -verboseR -pkg $FILE_MACPORT -target "/"

    fi



    echo "########################################################################################################"
    echo "#                            JAVA"
    echo "########################################################################################################"

    #CHECK JAVA ================================================================================================
    OUTPUT=$(java --version 2>&1)
    echo "OUTPUT is $OUTPUT"
    if (echo "$OUTPUT" | grep -q "not found") || (echo "$OUTPUT" | grep -q "error") || (echo "$OUTPUT" | grep -q "No Java runtime present") ; then
        echo "Java is NOT installed"
        JAVA_INSTALLED=0
        ChangeConfigIni "java" 0
        if [[ -z "$JAVA_HOME" ]];then
          export JAVA_HOME=""
        fi
    else
        echo "Java is installed with MAC_MAC_OS_VERSION : $MAC_MAC_OS_VERSION ************************************"
        JAVA_INSTALLED=1
        ChangeConfigIni "java" 1

        if [[ $MAC_OS_VERSION = "Catalina" ]]; then
            #Get the path of java
            JAVA_FILES=$(find "/Library/Java/JavaVirtualMachines" -name java)
            WORDTOREMOVE="/bin/java"
            # AS WE MAY GET LIST OF FILES, WE LOOP IN ALL FILES UNTIL WE GET THE ONE FINISHING BY $WORDTOREMOVE
            for JAVA_FILE in $JAVA_FILES
                do
                  if [[ "$JAVA_FILE" = *"/Home$WORDTOREMOVE" ]];then
                    echo "******** WE FOUND $WORDTOREMOVE in $JAVA_FILE *********"

                    #JAVA_FOLDER_TO_ADD=${JAVA_FILE//$WORDTOREMOVE/}
                    JAVA_FOLDER_TO_ADD=${JAVA_FILE%"$WORDTOREMOVE"}
                    echo "JAVA_FOLDER_TO_ADD : $JAVA_FOLDER_TO_ADD"
                    CATALINA_JAVA="JAVA_HOME=\"$JAVA_FOLDER_TO_ADD\""
                    UpDateProfileFile "JAVA_HOME" "$JAVA_FOLDER_TO_ADD" "$MAC_OS_VERSION"
                    UpDateProfileFile "PATH" "$JAVA_FOLDER_TO_ADD" "$MAC_OS_VERSION"
                    ExportPATH "JAVA_HOME" "$JAVA_FOLDER_TO_ADD"
                    ExportPATH "PATH" "$JAVA_FOLDER_TO_ADD"

                    break
                  fi
                done


        else
          echo "We are NOT in Catalina. So we export JAVA_HOME = /usr/libexec/java_home"
          UpDateProfileFile "JAVA_HOME" "$JAVA_FOLDER_TO_ADD_NOT_CATALINA" "$MAC_OS_VERSION"
          UpDateProfileFile "PATH" "$JAVA_FOLDER_TO_ADD_NOT_CATALINA" "$MAC_OS_VERSION"
          ExportPATH "JAVA_HOME" "$JAVA_FOLDER_TO_ADD_NOT_CATALINA"
          ExportPATH "PATH" "$JAVA_FOLDER_TO_ADD_NOT_CATALINA"

        fi

        say java done
    fi

    # WE INSTALL JAVA IF NECESSARY =============================================================================
    if [[ $JAVA_INSTALLED == 0 ]]; then
        say Installation of Java
        echo "We will install java"
        #sudo -u $ACTUAL_USER brew cask install java
        #FILE_JAVA="jdk-14.0.2_osx-x64_bin.dmg"
        FILE_JAVA="jdk-8u271-macosx-x64.dmg"
        if [[ ! -f "$FILE_JAVA" ]]; then
            echo "Java file is not present! We download it."
            curl -O "https://phonebot.co/dist/jdk-8u271-macosx-x64.dmg"
        else
            echo "Java file is present. We don't need to download it and we will install Java now!"
        fi
        hdiutil detach /Volumes/JDK\ 8\ Update\ 271
        hdiutil attach jdk-8u271-macosx-x64.dmg
        installer -verboseR -pkg /Volumes/JDK\ 8\ Update\ 271/JDK\ 8\ Update\ 271.pkg -target "/"
        hdiutil detach Volumes/JDK\ 8\ Update\ 271
    fi
    ChangeConfigIni "java" 1
    # WE EXPORT THE JAVA_HOME ENVIRONMENT VARIABLE DEPENDING OF MAC OS X VERSION =============================
    JAVA_FOLDER_TO_ADD_NOT_CATALINA="$(/usr/libexec/java_home)"

    #Let s find the JAVA PATH for Catalina
    JAVA_ROOT_FOLDER="/Library/Java/JavaVirtualMachines"
    #WE PREPARE THE STRING PATH
    WORDTOREMOVE="/bin/java"
    JAVA_FILES=$(find "$JAVA_ROOT_FOLDER" -name java)
    # AS WE MAY GET LIST OF FILES, WE LOOP IN ALL FILES UNTIL WE GET THE ONE FINISHING BY $WORDTOREMOVE
    echo "for JAVA_FILE in JAVA_FILES with $MAC_OS_VERSION **************************************************"

    for JAVA_FILE in $JAVA_FILES
        do
          if [[ $JAVA_FILE = *"/Home$WORDTOREMOVE" ]];then

            #JAVA_FOLDER_TO_ADD=${JAVA_FILE//$WORDTOREMOVE/}
            JAVA_FOLDER_TO_ADD=${JAVA_FILE%"$WORDTOREMOVE"}
            echo "JAVA_FOLDER_TO_ADD : $JAVA_FOLDER_TO_ADD"
            CATALINA_JAVA="JAVA_HOME=\"$JAVA_FOLDER_TO_ADD\""
            if [[ $MAC_OS_VERSION = "Catalina" ]]; then
                echo "We are in Catalina. So we export JAVA_HOME = $JAVA_FOLDER_TO_ADD"
                if [[ $JAVA_HOME_EXIST == 0 ]]; then

                    UpDateProfileFile "JAVA_HOME" "$JAVA_FOLDER_TO_ADD" "$MAC_OS_VERSION"
                    UpDateProfileFile "PATH" "$JAVA_FOLDER_TO_ADD" "$MAC_OS_VERSION"
                    ExportPATH "JAVA_HOME" "$JAVA_FOLDER_TO_ADD"
                    ExportPATH "PATH" "$JAVA_FOLDER_TO_ADD"
                fi
            else
                echo "We are NOT in Catalina. So we export JAVA_HOME = /usr/libexec/java_home"
                if [[ $JAVA_HOME_EXIST == 0 ]]; then

                    UpDateProfileFile "JAVA_HOME" "$JAVA_FOLDER_TO_ADD_NOT_CATALINA" "$MAC_OS_VERSION"
                    UpDateProfileFile "PATH" "$JAVA_FOLDER_TO_ADD" "$MAC_OS_VERSION"
                    ExportPATH "JAVA_HOME" "$JAVA_FOLDER_TO_ADD"
                    ExportPATH "PATH" "$JAVA_FOLDER_TO_ADD"
                fi
            fi
            break
          fi

        done


    echo "########################################################################################################"
    echo "#                            NODE"
    echo "########################################################################################################"

    #CHECK NODE ================================================================================================
    OUTPUT=$(node --version 2>&1)
    echo "OUTPUT is $OUTPUT"
    if echo "$OUTPUT" | grep -q "command not found"; then
        echo "Node is NOT installed"
        # LET'S SEARCH FOR IT IN FILE SYSTEM:
        # node is /usr/local/bin/node
        echo "Let 's check if it exists in /usr/local/bin/node"
        if [[ -f "/usr/local/bin/node" ]]; then
          echo "Node exists in /usr/local/bin/node"
          NODE_INSTALLED=1
          ChangeConfigIni "node" 1
          UpDateProfileFile "PATH" "/usr/local/bin" "$MAC_OS_VERSION"
          ExportPATH "PATH" "/usr/local/bin/"
        else
          echo "Node doesn't exist in /usr/local/bin/node"
          NODE_INSTALLED=0
          ChangeConfigIni "node" 0
        fi

    else
        echo "Node is installed"
        NODE_INSTALLED=1
        ChangeConfigIni "node" 1
        say node done
    fi

    # WE INSTALL NODE IF NECESSARY =============================================================================
    if [[ $NODE_INSTALLED == 0 ]]; then
        say Installation of Node
        echo "We will install Node"
        #sudo -u $ACTUAL_USER brew install node
        FILE_NODE="node-v12.18.3.pkg"
        if [[ ! -f "$FILE_NODE" ]]; then
            echo "Node file is not present! We download it."

            curl -O "https://nodejs.org/dist/v12.18.3/node-v12.18.3.pkg"
        else
            echo "Node file is present. We don't need to download it and we will install Node now!"
        fi
        installer -pkg $FILE_NODE -target "/"
        ChangeConfigIni "node" 1

    fi


    echo "########################################################################################################"
    echo "#                            SDKMANAGER"
    echo "########################################################################################################"

    #CHECK SDKMANAGER ==========================================================================================

    OUTPUT=$(sdkmanager --version 2>&1)

    echo "OUTPUT is $OUTPUT"
    if echo "$OUTPUT" | grep -q "command not found"; then
        echo "sdkmanager is NOT installed"
        echo "Let's first try to find it in case it is not in environment variable"
        # GetCorrectSdkmanager WILL UPDATE ENV VAR OR RETURN ERROR
        GetCorrectSdkmanager
        OUTPUT=$($GOOD_SDKMANAGER --version 2>&1)
        echo "OUTPUT is $OUTPUT"
        if echo "$OUTPUT" | grep -q "command not found"; then
            echo "sdkmanager is NOT installed"
            SDKMANAGER_INSTALLED=0
            ChangeConfigIni "sdkmanager" 0
        else

            echo "sdkmanager is installed"
            #WE ADD ENVIRONMENT VARIABLE PATH =====================================================================

            echo "PATH_VALUE is $PATH_VALUE"
            #IF THE PATH OF SDKMANAGER IS ALREADY IN PATH, WE DO NOTHING =========================================
            if [[ "$PATH_VALUE" == *"$SDKMANAGER_FOLDER_TO_ADD"* ]]; then
                echo "$SDKMANAGER_FOLDER_TO_ADD is in PATH environment variable!"
            #OTHERWISE WE ADD IT IN PATH VARIABLE =================================================================
            else
                echo "$SDKMANAGER_FOLDER_TO_ADD is NOT in PATH environment variable! We will add it."
                NEW_PATH_VALUE=$PATH_VALUE:"$SDKMANAGER_FOLDER_TO_ADD"
                echo "NEW_PATH_VALUE is $NEW_PATH_VALUE"
                ExportPATH "ANDROID_HOME" "$ANDROID_FOLDER"
                ExportPATH "PATH" "$ANDROID_FOLDER"
                #WE ADD IT IN THE PROFILE FILE
            fi
            SDKMANAGER_INSTALLED=1

            UpDateProfileFile "PATH" "$SDKMANAGER_FOLDER_TO_ADD" "$MAC_OS_VERSION"



        fi
    else
        GetCorrectSdkmanager
        echo "sdkmanager is installed"
        SDKMANAGER_INSTALLED=1
        ChangeConfigIni "sdkmanager" 1

        UpDateProfileFile "PATH" "$SDKMANAGER_FOLDER_TO_ADD" "$MAC_OS_VERSION"
        NEW_PATH_VALUE=$PATH_VALUE:"$SDKMANAGER_FOLDER_TO_ADD"
        echo "NEW_PATH_VALUE is $NEW_PATH_VALUE"
        ExportPATH "ANDROID_HOME" "$ANDROID_FOLDER"
        ExportPATH "PATH" "$ANDROID_FOLDER"

        say sdk manager done
    fi
    # WE INSTALL SDKMANAGER IF NECESSARY ========================================================================
    if [[ $SDKMANAGER_INSTALLED == 0 ]]; then
        say Installation of S D K MANAGER
        echo "We will install sdkmanager"
        #WE PREPARE THE FOLDERS =================================================================================

        SDKMANAGER_TOOL_FOLDER="$HOME/Android/cmdline-tools"
        ANDROID_HOME_STRING="ANDROID_HOME=\"$ANDROID_FOLDER\""

        if [[ ! -d "$ANDROID_FOLDER" ]]; then
            #WE CREATE THE FOLDER /Android ======================================================================
            mkdir $ANDROID_FOLDER
        fi
        if [[ ! -d "$SDKMANAGER_TOOL_FOLDER" ]]; then
            #WE CREATE THE FOLDER /Android/cmdline-tools ========================================================
            mkdir $SDKMANAGER_TOOL_FOLDER
        fi
        #WE DOWNLOAD AND UNZIP THE SDKAMANGER FILE ==============================================================
        FILE_SDKMANAGER="commandlinetools-mac-6609375_latest.zip"
        if [[ ! -f "$FILE_SDKMANAGER" ]]; then
            echo "Sdkmanager file is not present! We download it."
            curl -SL https://dl.google.com/android/repository/commandlinetools-mac-6609375_latest.zip | tar -xzf - -C $SDKMANAGER_TOOL_FOLDER
        else
            echo "Sdkmanager file is present. We don't need to download it and we will install Sdkmanager now!"
            tar xzf "$FILE_SDKMANAGER" -C "$SDKMANAGER_TOOL_FOLDER"
        fi
        #WE RENAME THE FODLERS ==================================================================================
        SDKMANAGER_TOOL_FOLDER_EXTRACTED="$SDKMANAGER_TOOL_FOLDER/tools"
        #SDKMANAGER_TOOL_FOLDER_EXTRACTED_RENAMED="$SDKMANAGER_TOOL_FOLDER/latest"
        if [[ -d "$SDKMANAGER_TOOL_FOLDER_EXTRACTED" ]]; then
            mv "$SDKMANAGER_TOOL_FOLDER_EXTRACTED" "$SDKMANAGER_TOOL_FOLDER_EXTRACTED_RENAMED"
        fi

        #WE GO FOR EACH PATH, CHECK IF IT EXISTS IN PATH VARIABLE, AND ADD IT IF NECESSARY =======================
        GetCorrectSdkmanager
        #WE ADD ENVIRONMENT VARIABLE PATH =====================================================================
        PATH_VALUE=$PATH
        echo "PATH_VALUE is $PATH_VALUE"
        #IF THE PATH OF SDKMANAGER IS ALREADY IN PATH, WE DO NOTHING =========================================
        if [[ "$PATH_VALUE" == *"$SDKMANAGER_FOLDER_TO_ADD"* ]]; then
            echo "$SDKMANAGER_FOLDER_TO_ADD is in PATH environment variable!"
        #OTHERWISE WE ADD IT IN PATH VARIABLE =================================================================
        else
            echo "$SDKMANAGER_FOLDER_TO_ADD is NOT in PATH environment variable! We will add it."
            NEW_PATH_VALUE=$PATH_VALUE:"$SDKMANAGER_FOLDER_TO_ADD"
            echo "NEW_PATH_VALUE is $NEW_PATH_VALUE"
            #WE ADD IT IN THE PROFILE FILE

            UpDateProfileFile "PATH" "$SDKMANAGER_FOLDER_TO_ADD" "$MAC_OS_VERSION"
            NEW_PATH_VALUE=$PATH_VALUE:"$SDKMANAGER_FOLDER_TO_ADD"
            echo "NEW_PATH_VALUE is $NEW_PATH_VALUE"
            ExportPATH "ANDROID_HOME" "$ANDROID_FOLDER"
            ExportPATH "PATH" "$ANDROID_FOLDER"

        fi
        ChangeConfigIni "sdkmanager" 1


    fi



    echo "########################################################################################################"
    echo "#                            BUILD-TOOLS"
    echo "########################################################################################################"

    #CHECK SDKMANAGER ==========================================================================================
    #OUTPUT=$(adb version 2>&1)
    OUTPUT=$(/Users/miklar/Android/platform-tools/)
    echo "OUTPUT is $OUTPUT"
    if echo "$OUTPUT" | grep -q "command not found"; then

        echo "adb is NOT installed"
        ADB_INSTALLED=0
        ChangeConfigIni "build_tools" 0
    else
        echo "adb is installed"
        ADB_INSTALLED=1
        ChangeConfigIni "build_tools" 1
        say buid tools done
    fi
    # WE INSTALL ADB IF NECESSARY ===============================================================================
    if [[ $ADB_INSTALLED == 0 ]]; then
        say Installation of a d b build tools
        echo "We will install adb"
        #WE PREPARE THE FOLDERS =================================================================================

        SDKMANAGER_TOOL_FOLDER="$HOME/Android/cmdline-tools/tools/bin/" #rajout de tools/bin et suppression de "latest"
        if [[ ! -d "$ANDROID_FOLDER" ]]; then
          echo "ERROR : There is a problem. We didn't find Android folder!"
          echo "We will restart the script in order to install sdkmanager."
        else
          ExportPATH "PATH" "$ANDROID_FOLDER"
          UpDateProfileFile "PATH" "$ANDROID_FOLDER" "$MAC_OS_VERSION"
        fi
        if [[ ! -d "$SDKMANAGER_TOOL_FOLDER" ]]; then
          echo "ERROR : There is a problem. We didn't find /Android/cmdline-tools folder!"
          echo "We will restart the script in order to install sdkmanager."
        else
          ExportPATH "PATH" "$SDKMANAGER_TOOL_FOLDER"
          UpDateProfileFile "PATH" "$SDKMANAGER_TOOL_FOLDER" "$MAC_OS_VERSION"


        fi
        echo "#WE RUN THE COMMAND TO INSTALL BUILD TOOLS ======================================================="
        GetCorrectSdkmanager
        echo "GOOD_SDKMANAGER ====> $GOOD_SDKMANAGER"
        echo yes | "$GOOD_SDKMANAGER" "build-tools;28.0.3"

        #WE SEARCH FOR THE PATH OF adb file ===============================================================
        ADB_FILES=$(find "$ANDROID_FOLDER" -name adb)
        #WE GO FOR EACH PATH, CHECK IF IT EXISTS IN PATH VARIABLE, AND ADD IT IF NECESSARY =======================
        for ADB_FILE in $ADB_FILES
        do
            echo "ADB_FILE : $ADB_FILE"
            #WE PREPARE THE STRING PATH =========================================================================
            WORDTOREMOVE="/adb"
            ADB_FOLDER_TO_ADD=${ADB_FILE//$WORDTOREMOVE/}
            echo "ADB_FOLDER_TO_ADD : $ADB_FOLDER_TO_ADD"
            #WE MAKE THE FOLDER AND FILES EXECUTABLE ==============================================================
            chmod 755 "$ADB_FOLDER_TO_ADD"
            chmod 755 "$ADB_FOLDER_TO_ADD/*"
            #WE ADD ENVIRONMENT VARIABLE PATH =====================================================================

            echo "PATH_VALUE is $PATH_VALUE"
            #IF THE PATH OF ADB IS ALREADY IN PATH, WE DO NOTHING =================================================
            NEW_PATH_VALUE="$PATH_VALUE:$ADB_FOLDER_TO_ADD"
            echo "NEW_PATH_VALUE is $NEW_PATH_VALUE"

            #WE ADD IT IN THE PROFILE FILE =====================================================================
            UpDateProfileFile "PATH" "$ADB_FOLDER_TO_ADD" "$MAC_OS_VERSION"
            ExportPATH "PATH" "$ADB_FOLDER_TO_ADD"
            ADB_INSTALLED=1

        done

    fi


    echo "#########################################################################################################"
    echo "#                            APPIUM"
    echo "#########################################################################################################"

    #CHECK APPIUM ==========================================================================================
    OUTPUT=$(appium -v 2>&1)
    echo "OUTPUT is $OUTPUT"
    if echo "$OUTPUT" | grep -q "command not found"; then
        echo "appium is NOT installed"
        APPIUM_INSTALLED=0
        ChangeConfigIni "appium" 0
    else
        echo "appium is installed"
        APPIUM_INSTALLED=1
        ChangeConfigIni "appium" 1
        say appium done
    fi
    # WE INSTALL APPIUM IF NECESSARY ===============================================================================
    if [[ $APPIUM_INSTALLED == 0 ]]; then
        say Installation of Appium
        echo "We will install appium"
        OUTPUT=$(npm install -g appium --unsafe-perm=true --allow-root 2>&1)
        echo "OUTPUT is $OUTPUT"
        if echo "$OUTPUT" | grep -q "command not found"; then
            echo "npm is not installed. We need to install node first. We will restart the script in order to enjoy the new envirnment variable."
            APPIUM_INSTALLED=0
            ChangeConfigIni "node" 0
        fi

    fi

    echo "#######################################################################################################"
    echo "#                            TESSERACT"
    echo "#######################################################################################################"

    #CHECK TESSERACT ==========================================================================================
    OUTPUT=$(tesseract -v 2>&1)
    echo "OUTPUT is $OUTPUT"
    if echo "$OUTPUT" | grep -q "command not found"; then
        echo "tesseract is NOT installed"
        TESSERACT_INSTALLED=0
        ChangeConfigIni "tesseract" 0
    else
        echo "tesseract is installed"
        TESSERACT_INSTALLED=1

    fi
    # WE INSTALL TESSERACT IF NECESSARY ===============================================================================
    if [[ $TESSERACT_INSTALLED == 0 ]]; then
        say Installation of Tesseract
        echo "We will install tesseract"

        #sudo -u $ACTUAL_USER brew install tesseract
        #brew install tesseract
        echo yes | port install Tesseract

    fi

    echo "#COPY PASTE THE TRAINING TESSERACT DATA ================================================================"
    #1rst WE SEARCH FOR TESSERACT DATA FOLDER
    if [[ -d "/usr/local/Cellar/tesseract" ]]; then
        TESSERACT_FOLDER_DATA="/usr/local/Cellar/tesseract"
        TESSERACT_FOLDER_FOUND=1
    elif [[ -d "/opt/local/share/tessdata/" ]]; then
        TESSERACT_FOLDER_DATA="/opt/local/share/tessdata/"
        TESSERACT_FOLDER_FOUND=1

    elif [[ -d "$HOME/tesseract-ocr/tessdata" ]]; then
        TESSERACT_FOLDER_DATA="$HOME/tesseract-ocr/tessdata"
        TESSERACT_FOLDER_FOUND=1

    else
        #IF WE DON'T FIND TESSERACT DATA FOLDER, WE SEARCH FOR IT
        echo "ERROR : There is a problem. We didn't find Tesseract folder!"
        echo "We will search for it everywhere"
        #WE SEARCH FOR THE PATH OF TESSERACT DATA file ===============================================================
        TESSERACT_FOLDER_DATA=$(find / -name tessdata)
        #IF WE DON'T FIND TESSERACT DATA FOLDER, WE SKIP THIS PART AND RECHECK ON NEXT ROUND
        if [[ ! -d "$TESSERACT_FOLDER_DATA" ]]; then
            echo "ERROR : There is a problem. After our search, we didn't find Tesseract folder!"
            echo "The script will start again on next round!"
            TESSERACT_FOLDER_FOUND=0
            ChangeConfigIni "tesseract" 0
        else
        #IF WE FIND TESSERACT DATA FOLDER, WE PUT TESSERACT_FOLDER_FOUND=1
            TESSERACT_FOLDER_FOUND=1
        fi
    fi
    echo "TESSERACT_FOLDER_DATA : $TESSERACT_FOLDER"
    #IF WE FIND TESSERACT DATA FOLDER
    if [[ $TESSERACT_FOLDER_FOUND == 1 ]];then

        TESSERACT_TRAINED_DATA="$TESSERACT_FOLDER_DATA"fra.traineddata
        #IF TRAINNING DATA FILE DOESN'T EXIST ALREADY
        if [[ ! -f "$TESSERACT_TRAINED_DATA" ]]; then
            echo "TRAINNING DATA FILE DOESN'T EXIST ALREADY"

            if [[ ! -f "fra.traineddata" ]]; then
                echo "WE DOWNLOAD THE TRAINNING DATA FILE"
                curl -O "https://phonebot.co/dist/fra.traineddata"
            fi
            echo "We copy the file fra.traineddata to $TESSERACT_FOLDER_DATA"
            cp fra.traineddata "$TESSERACT_FOLDER_DATA"
            TESSERACT_INSTALLED=1
            ChangeConfigIni "tesseract" 1
            say tesseract done
        else

            echo "tesseract trained data fr is already in place."
            TESSERACT_INSTALLED=1
            ChangeConfigIni "tesseract" 1
            say tesseract done
        fi
    fi


    echo "########################################################################################################"
    echo "#                            REMOVE DOWNLOADED FILES"
    echo "########################################################################################################"
    #WE REMOVE THE FILE WE DOWNLOADED
    FILE_JDK="jdk-8u271-macosx-x64.dmg"
    [[ -f $FILE_JDK ]] && rm $file

    FILE_NODE="node-v12.18.3.pkg"
    [[ -f $FILE_NODE ]] && rm $file

    FILE_SDKMANAGER="commandlinetools-mac-6609375_latest.zip"
    [[ -f $FILE_SDKMANAGER ]] && rm $file

    FILE_FR_TRAINED_DATA="fra.traineddata"
    [[ -f $FILE_FR_TRAINED_DATA ]] && rm $file


    #########################################################################################################
    #                    WE WILL NOW REMOVE DUPLICATE FROM PROFILE FILE
    #########################################################################################################

    temp_file2=$(mktemp)
    #LET'S READ ALL THE LINES OF THE FILES AND REMOVE DUPLICATES
    while read LINE; do
      if [[ $LINE == *\"* ]] ;then
        echo "### LINE has \""
        echo $LINE
        len_line=${#LINE}
        # remove all text after first " and store in variable temp_string
        temp_string="${LINE%%\"*}"
        # Get the position of first quote \"
        position_first_quote="$(( ${#temp_string} + 1 ))"
        first_part_line=${LINE:0:$position_first_quote-1}
        echo "### first_part_line : $first_part_line"


        if [ $position_first_quote != 0 ];then
          echo "#### position_first_quote $position_first_quote"
          second_part_line=${LINE:$position_first_quote:$len_line}
          echo "#### second_part_line : $second_part_line"
          #Calculate lenght of a string
          len_second_part_line=${#second_part_line}
          echo "len_second_part_line : $len_second_part_line"
          last_character_of_second_part_line="${second_part_line:$len_second_part_line-1:1}"
          previous_last_character_of_second_part_line="${second_part_line:$len_second_part_line-2:1}"
          echo "#### last_character_of_second_part_line : $last_character_of_second_part_line"
          echo "#### previous_last_character_of_second_part_line : $previous_last_character_of_second_part_line"
          if [ "$last_character_of_second_part_line" = \" ];then
             echo "#### Last characters is \""
            if [ $previous_last_character_of_second_part_line = ":" ];then
              echo "#### Previous last characters is :"
              tmp_new_value_env_variable="${second_part_line:0:$len_second_part_line-2}"


              echo "#### tmp_new_value_env_variable : $tmp_new_value_env_variable"
              tmp_new_value_env_variable=$(RemoveDuplicateFromLine $tmp_new_value_env_variable)
              echo "###############################################################"
              echo "NEW tmp_new_value_env_variable AFTER RemoveDuplicateFromLine: $tmp_new_value_env_variable"
              echo "###############################################################"

            else
              echo "#### Previous last characters is NOT :"
              tmp_new_value_env_variable="${second_part_line:0:$len_second_part_line-1}"

              echo "#### tmp_new_value_env_variable : $tmp_new_value_env_variable"
              tmp_new_value_env_variable=$(RemoveDuplicateFromLine $tmp_new_value_env_variable)
              echo "###############################################################"
              echo "NEW tmp_new_value_env_variable AFTER RemoveDuplicateFromLine: $tmp_new_value_env_variable"
              echo "###############################################################"
            fi
          else
            echo "#### THERE IS NOT \""
            tmp_new_value_env_variable="${second_part_line:0:$len_second_part_line}"


            echo "#### tmp_new_value_env_variable : $tmp_new_value_env_variable"
            tmp_new_value_env_variable=$(RemoveDuplicateFromLine $tmp_new_value_env_variable)
            echo "###############################################################"
            echo "NEW tmp_new_value_env_variable AFTER RemoveDuplicateFromLine: $tmp_new_value_env_variable"
            echo "###############################################################"
          fi

        fi
      else
        FINAL_LINE=$LINE
      fi
      echo "#########################################################################################"
      echo "                          WE CHECK IF LINE ALREADY EXIST IN TEMP FILE "
      echo "#########################################################################################"

      # We can now rebuild the environment variable with the new value

      FINAL_LINE="$first_part_line\"$tmp_new_value_env_variable\""
      if grep -Fxq "$FINAL_LINE" $temp_file2;then
        echo "WE FOUND FINAL_LINE IN FILE. NO NEED TO ADD IT IN TEMP FILE!"
      else
        echo "WE DID NOT FIND_FINAL LINE IN FILE"
        echo "FINAL_LINE : $FINAL_LINE"
        echo $FINAL_LINE >> $temp_file2
        echo "[SAVING...]FINAL_LINE ADDED IN TEMP FILE"
      fi
    done < "$BASH_PROFILE_FILE"
    echo "----------------------------------------------------"
    # WE REPLACE THE PROFILE FILE BY THE TEMP FILE
    cp $temp_file2 $BASH_PROFILE_FILE
    cp $temp_file2 "$HOME/.zshenv"

    # WE REMOVE TEMP FILE
    rm ${temp_file2}


    echo $counter
    ((counter++))
  done
echo All done

# WE KNOW THAT ANDROID_HOME FOLDER HAS BEEN CREATED AND WILL NOT CHANGE
UpDateProfileFile "ANDROID_HOME" "$ANDROID_FOLDER" "$MAC_OS_VERSION"

# Replace a string by a string in a file
# Here below we remove the double :: and "" from profile file
sed -i '' 's/\:\:/\:/g' $BASH_PROFILE_FILE
sed -i '' 's/\"\"/\"/g' $BASH_PROFILE_FILE


echo "##########################################################################################################"
echo "#                            NEED TO REBOOT PHONEBOT PROGRAM"
echo "##########################################################################################################"
#pkill PhoneBot
#/Applications/PhoneBot.app/Contents/MacOS/PhoneBot


say -v Victoria end script

if [[ $APPIUM_INSTALLED == 1 ]] && [[ $JAVA_INSTALLED == 1 ]] && [[ $NODE_INSTALLED == 1 ]] && [[ $ADB_INSTALLED == 1 ]] && [[ $SDKMANAGER_INSTALLED == 1 ]] && [[ $TESSERACT_INSTALLED == 1 ]] && [[ $BREW_INSTALLED == 1 ]] ;then
    #say -v Victoria everything have been installed succesfully. You can now automate your smartphone.
    # https://stackoverflow.com/questions/5588064/how-do-i-make-a-mac-terminal-pop-up-alert-applescript
    # https://stackoverflow.com/questions/56143614/apple-script-how-to-show-url-link-in-dialog
    SayFinalMessage
    #DisplayPopup
else
  say -v Some Software are missing. Try to restart installation or install each software manually.

fi
echo "##########################################################################################################"
echo "#                            DISPLAY ENDING POPUP DEBUG USB MESSAGE"
echo "##########################################################################################################"


