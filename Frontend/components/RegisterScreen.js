import React from 'react';
import { connect } from 'react-redux';
import { AsyncStorage, TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';
import { addEmail } from '../actions/addEmail'
import Connection from '../utils/connect'
var styles = require('../style');

_storeData = async (email) => {
    try {
        /*
        Store registered email upon successful verification!
        */
        console.log("saving email: ", email);

        await AsyncStorage.setItem('registered', email)
    } catch (error) {
        // error saving data
        console.log('err');
    }
};

function save(email) {
    try {
        AsyncStorage.setItem('registered', email)
        console.log("saving email: ", email);
    } catch (error) {
        console.log("error", error);
    }
}

/* Register Screen */
// Screen shown to user to register an email, *and enter a code sent to their e-mail* ** => to-do

class RegisterScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            submit: false,
        }
    }
    static navigationOptions = {
        title: 'Welcome', header: null
    };

    setEmail = function (email) {
        this.setState({ submit: true });
        Connection.connect("register", "POST", { "email": email }, (result) => {
            console.log("res:", result);
            AsyncStorage.setItem('email', email)
                .then(res => this.setState({
                    email: email,
                    submit: true,
                }))
                .then(() => {
                    this.props.addEmail(email);
                    if (this.state.email !== '') {
                        this.props.navigation.navigate('Home');
                    }
                })
                .catch(err => {
                    console.log("ERROR: ", err);
                });
        });
    }

    render() {
        if (this.state.submit && this.state.email === '') {
            return <View><Text>Loading...</Text></View>
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
                            Submit{' '}
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