import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')

var NewSheetTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View></View>
                <ScrollView>
                </ScrollView>
                <View>
                    <View style={styles.textHolder}>
                        <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1 }}
                            placeholder="Title"
                            onChangeText={(text) => this.setState({ text })}
                            value={this.state.text} />
                        <TouchableOpacity style={styles.openButton} onPress={() => this.doneComposition()}>
                            <Text style={{ color: 'white', fontSize: 40 }}>Create</Text>
                        </TouchableOpacity>
                    </View>
                    <View style={styles.footer}>
                        <TouchableOpacity onPress={() => this.setState({ newCompo: false })} style={styles.navButton}>
                            <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </ImageBackground>
    )
}

export default NewSheetTemplate;