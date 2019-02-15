import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';

var styles = require('../style')


/* Profile Screen */
// Provides basic info regarding user's email, allows option to change given email

export default class ProfileScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
                <View>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> hey its ur profile screen </Text>
                </View>
                <ScrollView>
                    <Text>hello</Text>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Home')} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Home </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};
