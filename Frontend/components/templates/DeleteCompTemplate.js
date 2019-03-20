import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')

var DeleteCompTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View></View>
                <View>
                    <View style={styles.textHolder}>
                        <TextInput style={{ marginTop: 200, height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                            placeholder="Composition to Delete"
                            onChangeText={(deleteText) => this.setState({ deleteText })}
                            value={this.state.deleteText} />
                        <TouchableOpacity style={styles.openButton} onPress={() => this.doneDeleteComposition()}>
                            <Text style={{ color: 'white', fontSize: 40 }}>Delete</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
            <View style={styles.footer}>
                <TouchableOpacity onPress={() => this.setState({ deleteCompo: false })} style={styles.navButton}>
                    <Text style={{ color: 'white', fontSize: 40 }}> Back </Text>
                </TouchableOpacity>
            </View>
        </ImageBackground>
    )
}

export default DeleteCompTemplate;