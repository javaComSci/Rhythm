import React from 'react';
import { connect } from 'react-redux';
import { Alert, AsyncStorage, TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';
import { addEmail } from '../actions/addEmail';
import { addUser } from '../actions/addUserID';
import Connection from '../utils/connect';
import LoadingScreen from './LoadingScreen';
import VerifyScreenTemplate from './templates/VerifyScreenTemplate';
import RegisterScreenTemplate from './templates/RegisterScreenTemplate';

var styles = require('../style');

/*
to do: deal with incoming email
*/

/* Register Screen */
// Screen shown to user to register an email, *and enter a code sent to their e-mail* ** => to-do

class RegisterScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            submit: false,
            awaitingCode: false,
            loading: false,
            verfCode: '',
            pendingEmail: '',
            id: 524,
        }
    }
    static navigationOptions = {
        title: 'Welcome', header: null
    };

    saveEmailLocal = async (email, that) => {
        AsyncStorage.setItem("email", email)
            .then(data => that.setState({
                email: email,
                submit: true,
            }))
            .then(() => {
                that.props.addEmail(email);
                console.log("here")
                if (email !== '') {
                    that.props.navigation.navigate('Home');
                }
            })
            .catch(err => {
                console.log("ERROR: ", err);
            });
    }

    saveIDLocal = async (id, that) => {
        AsyncStorage.setItem("id", id.toString())
            .then(data => that.setState({
                id: id.toString(),
                submit: true,
            }))
            .then(() => {
                that.props.addUser(id.toString());
                console.log("here2")
            })
            .catch(err => {
                console.log("ERROR: ", err);
            });
    }

    verifyAccount = function (code) {
        const that = this;
        if (code == '') {
            Alert.alert("Please enter a verification code")
            return
        }
        fetch('http://18.237.79.152:5000/checkKey', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'code': code
            })
        }).then(res => {
            res.text().then(function (data) {
                console.log("pada", data)
                if (JSON.parse(data).id == -1) {
                    Alert.alert("Invalid verification code")
                }
                else {
                    console.log("added")
                    that.props.addUser(JSON.parse(data).id)
                    that.saveIDLocal(JSON.parse(data).id, that);
                    console.log("saved local?")
                    that.saveEmailLocal(that.state.pendingEmail, that)
                }
            })
        }).catch(err => {
            console.log("error", err)
        })
    }

    recoverAccount = function (email) {
        const that = this;
        if (email == '') {
            console.log('no email')
            Alert.alert("Please enter a valid email address")
            return
        }
        that.setState({
            loading: true
        })
        fetch('http://18.237.79.152:5000/recoverEmail', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'email': email
            })
        }).then(res => {
            res.text().then(function (data) {
                console.log("DATA:", data)
                if (data == 'sent') {
                    that.setState({
                        awaitingCode: true,
                        pendingEmail: email,
                        loading: false,
                    })
                }
                else {
                    Alert.alert("Please enter a valid email address")
                    this.setState({
                        loading: false
                    })
                }
            });
        }).catch(res => {
            console.log("error", res);
        })
    }

    setEmail = function (email) {
        const that = this;
        if (email == '') {
            Alert.alert("Please enter an email address");
            return;
        }
        fetch('http://18.237.79.152:5000/register', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'email': email
            }),
        }).then(res => {
            res.text().then(function (res) {
                console.log("RESULT FROM SETEMAIL", res);
                if (JSON.parse(res).ok == 'true') {
                    that.saveIDLocal(JSON.parse(res).id, that)
                    that.saveEmailLocal(email, that);
                }
                else {
                    Alert.alert("Email already in use.  Select recover account to get a code")
                }
            })
        })
            .catch(res => {
                console.log('bad', res)
            });
    }

    render() {
        if ((this.state.submit && this.state.email === '') || this.state.loading) {
            return <LoadingScreen />
        }
        if (this.state.awaitingCode) {
            return (
                VerifyScreenTemplate.call(this)
            )
        }
        return (
            RegisterScreenTemplate.call(this)
        );
    }
};

function mapStateToProps(state) {
    return {
        isRegistered: state.email,
        id: state.id
    }
}

function mapDispatchToProps(dispatch) {
    return {
        addEmail: email => dispatch(addEmail(email)),
        addUser: id => dispatch(addUser(id))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RegisterScreen);