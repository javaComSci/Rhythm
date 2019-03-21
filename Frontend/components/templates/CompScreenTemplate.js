import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';
import DialogInput from 'react-native-dialog-input';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')


var CompScreenTemplate = function () {
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <DialogInput isDialogVisible={this.state.isDialogVisible}
                    title={"Duplicate Composition"}
                    hintInput={"New Composition Name"}
                    submitInput={(inputText) => {
                        // edit title
                        // duplicate composition
                        this.duplicateComposition(inputText)
                        this.setState({ isDialogVisible: false, toEdit: '' })
                    }}
                    closeDialog={() => { this.setState({ isDialogVisible: false, toEdit: '' }) }}>
                </DialogInput>
                <View style={styles}>
                    <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> COMPOSITIONS </Text>
                    <View style={styles.lineBreak} />
                </View>
                <View style={styles.operatorContainer}>
                    <TouchableOpacity
                        onPress={() => this.createComposition()}
                        style={styles.addButton}
                    >
                        <Text style={styles.menuText}>+</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        onPress={() => this.deleteComposition()}
                        style={styles.minusButton}
                    >
                        <Text style={styles.menuText}>-</Text>
                    </TouchableOpacity>
                </View>
                <ScrollView>
                    <FlatList
                        data={this.state.compositions}
                        extraData={this.state}
                        renderItem={({ item }) =>
                            <View style={styles.compositionContainer}>
                                <TouchableOpacity
                                    onPress={() => this.props.navigation.navigate('ViewCompScreen', { 'compositionID': item.getID(), 'compositionTitle': item.getTitle(), 'compositionDescription': item.getDescription() })}
                                    style={styles.compositionItem}
                                    onLongPress={(e) => {
                                        this.setState({
                                            isDialogVisible: true,
                                            toEdit: [item.getTitle(), item.getID()], // getdescription actually gets the composition id
                                        })
                                    }}>
                                    <Text style={{ color: 'white', fontSize: 40 }}>{item.getTitle()}</Text>
                                </TouchableOpacity>
                                <View style={styles.lineBreak} />
                            </View>}
                    />
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Home')} style={styles.navButton}>
                        <Text style={styles.menuText}> Home </Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    )
}

export default CompScreenTemplate;