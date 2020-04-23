## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy
  - utter_can_i_help_you

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy
  - utter_can_i_help_you

## sad path 2
* greet
  - utter_greet
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
* currencies{"currency":"долар"}
 - action_check_currency
 - utter_can_i_help_you
 
 ## currency rate eur
* currency_exchange
  - utter_currencies
* currencies{"currency":"євро"}
 - action_check_currency
 - utter_can_i_help_you
 
## check info happy
* check_request
 - utter_check_ask
* check_num{"check_num":"976964496"}
 - action_get_cheque
 - utter_can_i_help_you
* affirm
 - utter_happy
 - utter_can_i_help_you
 
 ## check info sad
* check_request
 - utter_check_ask
* check_num{"check_num":"976964496"}
 - action_get_cheque
 - utter_can_i_help_you
* deny
 - utter_sad
 - utter_can_i_help
 
 
 ## hello
 * hello
  - action_say_hello
  - utter_can_i_help
  
## atm_info_happy
* ask_atm
  - utter_ask_address
* address_name{"latitude":"18.940170","longitude":"72.83486"}
 - action_atm_locator
 - utter_did_that_help
* affirm
 - utter_happy
 - utter_can_i_help_you

## atm_info_sad
* ask_atm
  - utter_ask_address
* address_name{"latitude":"18.940170","longitude":"72.83486"}
 - action_atm_locator
 - utter_did_that_help
 * deny
 - utter_can_i_help_you
