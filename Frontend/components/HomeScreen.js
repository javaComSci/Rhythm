import React from 'react';
import { AsyncStorage, TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';
import RegisterScreen from './RegisterScreen';

var styles = require('../style')

/*
load generated music files from local storage
*/
_storeData = async () => {
    try {
        /*
        AsyncStorage stores data in a dictionary
        */
        await AsyncStorage.setItem('testKey', 'testValue')
    } catch (error) {
        // error saving data
        console.log('err');
    }
};

_retrieveData = async () => {
    try {
        /*
        Retrieve data from AsyncStorage by key
        */
        const value = await AsyncStorage.getItem('testKey');
        if (value != null) {
            console.log("value", value);
        } else {
            // no item by key
            console.log("nothing here");
        }
    } catch (error) {
        console.log("error", error);
    }
}

_isLoggedIn = async () => {
    try {
        const value = await AsyncStorage.getItem("registere");
        console.log("value: ", value);
        if (value != null) {
            console.log('email:', value);
            return true;
        } else {
            console.log("no");
            return false;
        }
    } catch (error) {
        console.log("err: ", error);
    }
}

export default class HomeScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            userEmail: null,
        };
    }

    componentDidMount() {
        this.setState({ isLoading: true });
        AsyncStorage.getItem("email")
            .then(result => this.setState({
                isLoading: false, // set isLoading to false until item is retrieved
                userEmail: result ? result : "none", // if result was null, set email to none
            }))
            .then(() => {
                // if no email has been stored, go to register screen
                if (this.state.userEmail === "none") {
                    this.props.navigation.navigate("Register");
                }
            })
            .catch(error => this.setState({
                isLoading: false,
                userEmail: result,
            }))
    }
    static navigationOptions = {
        title: '', header: null // setting header to null to remove the default header from react-navigation
    };
    render() {
        if (this.state.isLoading) {
            return <View><Text>Loading...</Text></View>
        }
        else if (!this.state.userEmail)
            return <View><Text>Loading...</Text></View>
        return (
            <View style={styles.container}>
                <ScrollView>
                    <View style={styles.textHolder}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 75 }}> Rhythm </Text>
                    </View>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Composition')} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Compositions </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Profile')} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Profile </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};
