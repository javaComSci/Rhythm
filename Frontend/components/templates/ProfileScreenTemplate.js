import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View, Button, KeyboardAvoidingView, TextInput, ImageBackground } from 'react-native';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')


var ProfileScreenTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View>
                    <Text style={{ color: 'black', fontWeight: 'bold', fontSize: 75 }}> Profile </Text>
                </View>
                <ScrollView style={{ flex: 1, marginLeft: 50 }}>
                    <Text style={{ color: 'black', fontSize: 40 }}>{this.state.name} </Text>
                    <Text style={{ color: 'black', fontSize: 20 }}>{this.state.email} </Text>
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => this.editProfile()}
                        style={styles.navButton}
                    >
                        <Text style={{ color: 'white', fontSize: 40 }}> Edit </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => this.props.navigation.navigate('Home')}
                        style={styles.navButton}
                    >
                        <Text style={{ color: 'white', fontSize: 40 }}> Home </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    )
}

export default ProfileScreenTemplate;