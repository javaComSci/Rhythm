import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';
import DialogInput from 'react-native-dialog-input';

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')

var SheetScreenTemplate = function () {
    const { navigation } = this.props;
    const compositionID = navigation.getParam('compositionID', 'NO_ID');
    const compositionTitle = navigation.getParam('compositionTitle', 'NO_TITLE')
    const compositionDescription = navigation.getParam('compositionDescription', '')
    return (
        <ImageBackground source={background} style={{ width: '100%', height: '100%' }}>
            <View style={styles.container}>
                <DialogInput isDialogVisible={this.state.isDialogVisible}
                    title={"Edit Sheet Name"}
                    hintInput={"New Title"}
                    submitInput={(inputText) => {
                        // edit title
                        this.editSheet(inputText, this.state.toEdit[1])
                        this.setState({ isDialogVisible: false, toEdit: '' })
                    }}
                    closeDialog={() => { this.setState({ isDialogVisible: false, toEdit: '' }) }}>
                </DialogInput>
                <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40, width: "80%" }}> {compositionTitle} </Text>
                <View style={{height: 100}}>
                    <View style={styles.operatorContainer}>
                        <TouchableOpacity
                            onPress={() => this.createComposition()}
                            style={styles.addButton}
                        >
                            <Text style={styles.menuText}>+</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.neutralButton} onPress={() => this.setState({ "duplicateVisible": true })}>
                            <Text style={styles.buttonText}>Duplicate</Text>
                        </TouchableOpacity>
                        {/* <TouchableOpacity style={styles.neutralButton} onPress={() => this.props.navigation.navigate('EditMusicScreen', {title: ""})}>
                            <Text style={styles.buttonText}>Edit</Text>
                        </TouchableOpacity> */}
                        <TouchableOpacity style={styles.minusButton} onPress={() => this.deleteComposition()}>
                            <Text style={styles.menuText}>-</Text>
                        </TouchableOpacity>
                    </View>
                </View>

                <Text style={{ color: 'white', }}>{compositionDescription}</Text>
                <ScrollView>
                    <FlatList
                        data={this.state.sheet_music}
                        extraData={this.state}
                        renderItem={({ item }) =>
                            <View style={styles.compositionContainer}>
                                <TouchableOpacity
                                    style={styles.compositionItem}
                                    onPress={(e) => {
                                        this.props.navigation.navigate('EditMusicScreen', {title: item.getTitle(), file: item.getFile(), sheet_id: item.getID(), email: this.props.isRegistered})
                                    }}
                                    onLongPress={(e) => {
                                        console.log("pepper")
                                        this.setState({
                                            isDialogVisible: true,
                                            toEdit: [item.getTitle(), item.getID()], // getdescription actually gets the composition id
                                        })
                                    }}
                                >
                                    <Text style={{ color: 'white', fontSize: 40 }}>{item.getTitle()}</Text>
                                </TouchableOpacity>


                                <TouchableOpacity
                                    onPress={(e) => {
                                        this.props.navigation.navigate('SelectMusicScreen', {title: item.getTitle(), sheet_id: item.getID()})
                                    }}
                    
                                >
                                <Text> {item.getID()} </Text>
                                    <Text style={{ color: 'black', fontSize: 10 }}>Selected Instrument: PIANO</Text>
                                </TouchableOpacity>


                                <View style={styles.lineBreak} />
                            </View>}
                    />
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity
                        onPress={() => this.props.navigation.navigate('Composition')}
                        style={styles.navButton}
                    >
                        <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 40 }}> Back </Text>
                    </TouchableOpacity>
                </View>
            </View >
        </ImageBackground>
    )
}

export default SheetScreenTemplate;