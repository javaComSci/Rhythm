import React from 'react';
import { TouchableOpacity, ScrollView, StyleSheet, Text, View, Button, KeyboardAvoidingView, TextInput, ImageBackground } from 'react-native';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')


var ProfileEditTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View></View>
                <ScrollView>
                </ScrollView>
                <View>
                    <KeyboardAvoidingView keyboardVerticalOffset={-500} behavior="padding" style={styles.textHolder} enabled>
                        <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1, color: "white" }}
                            placeholder="Name"
                            onChangeText={(nameText) => this.setState({ nameText })}
                            value={this.state.nameText} />
                        <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1, color: "white" }}
                            placeholder="Email"
                            onChangeText={(emailText) => this.setState({ emailText })}
                            value={this.state.emailText} />
                    </KeyboardAvoidingView>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity
                        style={styles.navButton}
                        onPress={() => this.doneEdit()}
                    >
                        <Text style={{ color: 'white', fontSize: 40 }}> Submit </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => { this.setState({ edit: false, }) }}
                        style={styles.navButton}
                    >
                        <Text style={{ color: 'white', fontSize: 40 }}> Cancel </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    )
}

export default ProfileEditTemplate;