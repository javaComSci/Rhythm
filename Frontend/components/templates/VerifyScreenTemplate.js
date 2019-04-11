import React from 'react';
import { TextInput, TouchableOpacity, ScrollView, Text, View, ImageBackground } from 'react-native';
var background = require('../../assets/backgroundImage.png')
var styles = require('../../style')

var VerifyScreenTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View style={styles.header}>
                    <Text style={{ color: 'black', fontWeight: 'bold', fontSize: 40 }}>
                        Verification
        </Text>
                    <View style={styles.lineBreak} />
                </View>
                <ScrollView>
                    <View style={styles.inputContainer}>
                        <View style={{ alignItems: 'center', width: '90%' }}>
                            <Text
                                style={{ color: 'black', fontWeight: 'bold', fontSize: 40 }}>
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
                            style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}>
                            {' '}
                            Verify{' '}
                        </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    )
}

export default VerifyScreenTemplate;