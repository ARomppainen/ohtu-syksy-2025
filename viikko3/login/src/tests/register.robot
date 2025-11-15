*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  foobar
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  aa
    Set Password  foobar123
    Set Password Confirmation  foobar123
    Click Button  Register
    Register Should Fail With Message  Username too short (min 3 characters)

Register With Valid Username And Too Short Password
    Set Username  foobar1
    Set Password  short1
    Set Password Confirmation  short1
    Click Button  Register
    Register Should Fail With Message  Password too short (min 8 characters)

Register With Valid Username And Invalid Password
    Set Username  foobar2
    Set Password  invalidpassword
    Set Password Confirmation  invalidpassword
    Click Button  Register
    Register Should Fail With Message  Password invalid (it may not contain only letters)

Register With Nonmatching Password And Password Confirmation
    Set Username  foobar3
    Set Password  foobar123
    Set Password Confirmation  foobar456
    Click Button  Register
    Register Should Fail With Message  Password did not match the confirmation value

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists


*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

