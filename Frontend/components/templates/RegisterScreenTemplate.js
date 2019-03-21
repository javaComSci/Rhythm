import React from 'react';
import { TextInput, TouchableOpacity, ScrollView, Text, View, ImageBackground } from 'react-native';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')

var RegisterScreenTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View style={styles.header}>
                    <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}>
                        Register
              </Text>
                    <View style={styles.lineBreak} />
                </View>
                <ScrollView>
                    <View style={styles.inputContainer}>
                        <View style={{ alignItems: 'center', width: '90%' }}>
                            <Text
                                style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}>
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
                            style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}>
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
                            style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}>
                            {' '}
                            Recover Account{' '}
                        </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    )
}

export default RegisterScreenTemplate;
