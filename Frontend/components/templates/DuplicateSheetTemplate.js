import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';
import RNPickerSelect from 'react-native-picker-select';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')

var DuplicateSheetTemplate = function () {
    const placeholder = {
        label: 'Select sheet music...',
        value: null,
        color: "gray"
    };
    const placeholder2 = {
        label: 'Select composition...',
        value: null,
        color: "gray"
    };
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <View>
                    <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40, width: "80%" }}> Duplicate </Text>
                </View>
                <View>
                    <RNPickerSelect
                        placeholder={placeholder}
                        items={this.sheetList}
                        onValueChange={(value) => {
                            this.setState({
                                selectedSheet: value,
                            })
                        }}>
                    </RNPickerSelect>
                </View>
                <View style={styles.lineBreak} />
                <View>
                    <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 30, width: "80%" }}> Select composition </Text>
                </View>
                <View>
                    <RNPickerSelect
                        placeholder={placeholder2}
                        items={this.compList}
                        onValueChange={(value) => {
                            this.setState({
                                selectedComposition: value,
                            })
                        }}>
                    </RNPickerSelect>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.duplicateComposition()} style={styles.navButton}>
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> Submit </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.setState({ duplicateVisible: false })} style={styles.navButton}>
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    )
}

export default DuplicateSheetTemplate;