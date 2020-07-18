## hello
* hello
  - action_say_hello
  - utter_can_i_help
  
## chitchat happy
* chitchat
  - utter_happy
  - utter_greet
* mood_great
  - utter_happy
  - utter_can_i_help_you

## chitchat sad path 1
* chitchat
  - utter_happy
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy
  - utter_can_i_help_you

## chitchat sad path 2
* chitchat
  - utter_happy
  - action_say_hello
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
 - utter_sad
 - utter_can_i_help_you

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
  
## currency rate usd
* currency_exchange
  - utter_currencies
* inform{"currency":"долар"}
 - action_check_currency
 - utter_can_i_help_you
 
 ## currency rate eur
* currency_exchange
  - utter_currencies
* inform{"currency":"євро"}
 - action_check_currency
 - utter_can_i_help_you
 
## check info happy
* check_request
 - utter_check_ask
* inform{"check_num":"976964496"}
 - action_get_cheque
 - utter_can_i_help_you
* affirm
 - utter_happy
 - utter_can_i_help_you
 
 ## check info sad
* check_request
 - utter_check_ask
* inform{"check_num":"976964496"}
 - action_get_cheque
 - utter_can_i_help_you
* deny
 - utter_sad
 - utter_can_i_help
  
## atm_info_happy_latlon
* ask_atm
  - utter_ask_address
* inform{"latitude": "18.940170","longitude": "72.83486"}
 - action_atm_locator
 - utter_did_that_help
* affirm
 - utter_happy
 - utter_can_i_help_you
 

## atm_info_sad_latlon
* ask_atm
  - utter_ask_address
* inform{"latitude": "18.940170","longitude": "72.83486"}
 - action_atm_locator
 - utter_did_that_help
 * deny
 - utter_sad
 - utter_can_i_help_you

## atm_info_happy_location
* ask_atm
  - utter_ask_address
* inform{"location":"Ірпінь"}
 - action_atm_locator
 - utter_did_that_help
* affirm
 - utter_happy
 - utter_can_i_help_you

## atm_info_sad_location
* ask_atm
  - utter_ask_address
* inform{"location":"Харків"}
 - action_atm_locator
 - utter_did_that_help
 * deny
 - utter_sad
 - utter_can_i_help_you
 
 ## branch_info_happy_latlon
* ask_branch
  - utter_ask_address
* inform{"latitude": "18.940170","longitude": "72.83486"}
 - action_branch_locator
 - utter_did_that_help
* affirm
 - utter_happy
 - utter_can_i_help_you

## branch_info_sad_latlon
* ask_branch
  - utter_ask_address
* inform{"latitude": "18.940170","longitude": "72.83486"}
 - action_branch_locator
 - utter_did_that_help
 * deny
 - utter_sad
 - utter_can_i_help_you

## branch_info_happy_location
* ask_branch
  - utter_ask_address
* inform{"location":"Ірпінь"}
 - action_branch_locator
 - utter_did_that_help
* affirm
 - utter_happy
 - utter_can_i_help_you

## branch_info_sad_location
* ask_branch
  - utter_ask_address
* inform{"location":"Харків"}
 - action_branch_locator
 - utter_did_that_help
 * deny
 - utter_sad
 - utter_can_i_help_you

## fallback_story
* out_of_scope 
 - action_time_check
 - action_default_fallback

## carousel_story_1
* carousel
 - action_carousel
* deny
 - utter_sad
 - utter_can_i_help_you

## carousel_story_2
* carousel
 - action_carousel
* affirm
 - utter_happy
 - utter_can_i_help_you
  
## interactive_story_1
* hello
    - action_say_hello
    - utter_can_i_help_you
* ask_atm
    - utter_ask_address
* inform{"location": "Ірпінь"}
    - slot{"location": "Ірпінь"}
    - action_atm_locator
    - utter_did_that_help
* currency_exchange
    - utter_currencies
* inform{"currency": "євро"}
    - slot{"currency": "євро"}
    - action_check_currency
    - utter_can_i_help_you
* ask_branch
    - utter_ask_address
* inform{"latitude": "51.034067", "longitude": "31.875736"}
    - slot{"latitude": "51.034067"}
    - slot{"longitude": "31.875736"}
    - action_branch_locator
    - utter_did_that_help
* check_request
    - utter_check_ask
* inform{"check_num": "0976964496"}
    - slot{"check_num": "0976964496"}
    - action_get_cheque
    - utter_can_i_help_you

## interactive_story_1
* hello
    - action_say_hello
    - utter_can_i_help_you
* carousel
    - action_carousel
