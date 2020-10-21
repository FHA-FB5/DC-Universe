#!/bin/bash

# setup
tmux_session_bot=dcUniverseBot
repository_url=https://github.com/FHA-FB5/DC-Universe.git

# get applicatio dir and switch to it
application_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $application_dir

# check for test mode
if [ -f "testMode" ]
then
    test_mode=true
    echo "Info: Script is executed in test mode"
else
    test_mode=false
fi

# all functions
start() {
    echo "Start bot..."
	tmux new-session -d -s $tmux_session_bot \; send-keys "cd $application_dir ;python3 run.py" Enter
}
stop() {
    echo "Stop bot..."
	tmux kill-session -t $tmux_session_bot
}
restart() {
    start
    stop
}

# functions
function update_files {
    # start
    echo "Update files..."
    
    if [ $test_mode == true ]
    then
        echo "Info: Download is not executed (test mode activated)"
    else
	    cd $application_dir
        git clone $repository_url tmp
        cp -a tmp/* $application_dir
        chmod +x bot.sh
        rm -rf tmp
    fi

    # end
    echo "Success: Update completed"
}
function update_requirements {
    # start
    echo "Update requirements..."

    # install all requirements
	pip3 install -r requirements.txt

    # end
    echo "Success: Update completed"
}
function update_database {
    # start
    echo "Update database..."

    # update database
    alembic upgrade head

    # end
    echo "Success: Update completed"
}
function update_all {
    update_files
    update_requirements
    update_database
}
function test_mode {
    # check if config file exist
    if [ $test_mode == true ]
    then
        echo "Info: Test mode file was found"
    else
        echo "Info: Test mode file was not found"

        # create test mode file
        echo "Create test mode file..."
        touch testMode
        echo "Success: Creation completed"
    fi
}

# check command
case $1 in 
    "--start" )
        start
        ;;
    "--stop" )
        stop
        ;;
    "--restart" )
        restart
        ;;
    "--update" )
        # check mode
        case $2 in
            "--files"|"-f" )
                update_files
                ;;
            "--requirements"|"-r" )
                update_requirements
                ;;
            "--database"|"-db" )
                update_database
                ;;
            "--all"|"-a" )
                update_all
                ;;
            *)
                echo "Error: Your input was incorrect, please have a look at the list of all commands here: https://github.com/FHA-FB5/DC-Universe/wiki/bot.sh"
                exit 1
                ;;
        esac
        ;;
    "--dev" )
        # check mode
        case $2 in
            "--testmode" )
                test_mode
                ;;
            *)
                echo "Error: Your input was incorrect, please have a look at the list of all commands here: https://github.com/FHA-FB5/DC-Universe/wiki/bot.sh"
                exit 1
                ;;
        esac
        ;;
    "--test" )
        #does nothing
        ;;
    *)
        echo "Error: Your input was incorrect, please have a look at the list of all commands here: https://github.com/FHA-FB5/DC-Universe/wiki/bot.sh"
        exit 1
        ;;
esac
