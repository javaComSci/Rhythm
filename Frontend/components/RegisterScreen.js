import React from 'react';
import { connect } from 'react-redux';
import { Alert, AsyncStorage, TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';
import { addEmail } from '../actions/addEmail'
import Connection from '../utils/connect'
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
            verfCode: '',
        }
    }
    static navigationOptions = {
        title: 'Welcome', header: null
    };

    verifyAccount = function (code) {
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
                console.log(data)
                if (JSON.parse(data).id == -1) {
                    Alert.alert("Invalid verification code")
                }
                else {
                    console.log("User id:", JSON.parse(data).id)
                    // do something
                    // todo
                    // store this or something
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
                console.log("data:", data)
                if (data == 'sent') {
                    that.setState({
                        awaitingCode: true
                    })
                }
                else {
                    Alert.alert("Please enter a valid email address")
                }
            });
        }).catch(res => {
            console.log("error", res);
        })
    }

    setEmail = function (email) {
        const that = this;
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
                if (JSON.parse(res).ok == 'true') {
                    AsyncStorage.setItem('email', email)
                        .then(data => that.setState({
                            email: email,
                            submit: true,
                        }))
                        .then(() => {
                            that.props.addEmail(email);
                            if (that.state.email !== '') {
                                that.props.navigation.navigate('Home');
                            }
                        })
                        .catch(err => {
                            console.log("ERROR: ", err);
                        });
                }
            })
        })
            .catch(res => {
                console.log('bad', res)
            });
    }

    render() {
        if (this.state.submit && this.state.email === '') {
            return <View><Text>Loading...</Text></View>
        }
        if (this.state.awaitingCode) {
            return (
                <View style={styles.container}>
                    <View style={styles.header}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                            Verification
                        </Text>
                        <View style={styles.lineBreak} />
                    </View>
                    <ScrollView>
                        <View style={styles.inputContainer}>
                            <View style={{ alignItems: 'center', width: '90%' }}>
                                <Text
                                    style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                                    Verification Code:
                                </Text>
                            </View>
                            <TextInput
                                style={{
                                    width: '90%',
                                    height: 40,
                                    color: '#f19393',
                                    borderColor: '#f19393',
                                    borderWidth: 1,
                                    fontWeight: 'bold',
                                }}
                                onChangeText={text => this.setState({ verfCode: text })}
                                value={this.state.verfCode}
                            />
                        </View>
                    </ScrollView>
                    <View style={styles.footer}>
                        <TouchableOpacity
                            onPress={() => {
                                this.verifyAccount(this.state.verfCode)
                            }}
                            style={styles.navButton}>
                            <Text
                                style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                                {' '}
                                Verify{' '}
                            </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            )
        }
        return (
            <View style={styles.container}>
                <View style={styles.header}>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                        Register
              </Text>
                    <View style={styles.lineBreak} />
                </View>
                <ScrollView>
                    <View style={styles.inputContainer}>
                        <View style={{ alignItems: 'center', width: '90%' }}>
                            <Text
                                style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                                Email:
                            </Text>
                        </View>
                        <TextInput
                            style={{
                                width: '90%',
                                height: 40,
                                color: '#f19393',
                                borderColor: '#f19393',
                                borderWidth: 1,
                                fontWeight: 'bold',
                            }}
                            onChangeText={text => this.setState({ email: text })}
                            value={this.state.email}
                        />
                    </View>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => {
                            this.setEmail(this.state.email)
                        }}
                        style={styles.navButton}>
                        <Text
                            style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                            {' '}
                            Register Email{' '}
                        </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => {
                            this.recoverAccount(this.state.email)
                        }}
                        style={styles.navButton}>
                        <Text
                            style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                            {' '}
                            Recover Account{' '}
                        </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};

function mapStateToProps(state) {
    return {
        isRegistered: state.email
    }
}

function mapDispatchToProps(dispatch) {
    return {
        addEmail: email => dispatch(addEmail(email))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RegisterScreen);