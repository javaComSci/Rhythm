import React from 'react';
import { AsyncStorage, TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';

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

export default class RegisterScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
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
                            onChangeText={text => this.setState({ text })}
                            value={""}
                        />
                    </View>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => {
                            save("test@email.com")
                            this.props.navigation.navigate('Home')
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
