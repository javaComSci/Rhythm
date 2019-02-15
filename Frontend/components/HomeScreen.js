import React from 'react';
import { AsyncStorage, TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';

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

export default class HomeScreen extends React.Component {
    static navigationOptions = {
        title: '', header: null // setting header to null to remove the default header from react-navigation
    };
    render() {
        return (
            <View style={styles.container}>
                <ScrollView>
                    <View style={styles.textHolder}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 75 }}> Rhythm </Text>
                    </View>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => _storeData()} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> save data </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => _retrieveData()} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> read data </Text>
                    </TouchableOpacity>
                </View>
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
