import React from 'react';
import { Alert, AsyncStorage, TouchableOpacity, ScrollView, StyleSheet, Text, View } from 'react-native';

var styles = require('../../style')

var HomeScreenTemplate = function () {
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
            <View style={styles.footer}>
                <TouchableOpacity onPress={() => this.takeAndUploadPhotoAsync()} style={styles.navButton}>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Camera </Text>
                </TouchableOpacity>
            </View>
            <View style={styles.footer}>
                <TouchableOpacity onPress={() => this.clearCache()} style={styles.navButton}>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Clear Cache </Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

export default HomeScreenTemplate;
