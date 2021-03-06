import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView, ImageBackground } from 'react-native';
import DialogInput from 'react-native-dialog-input';
import Icon from 'react-native-vector-icons/AntDesign'

var styles = require('../../style')
var background = require('../../assets/backgroundImage.png')

var SheetScreenTemplate = function () {
    const { navigation } = this.props;
    const compositionID = navigation.getParam('compositionID', 'NO_ID');
    const compositionTitle = navigation.getParam('compositionTitle', 'NO_TITLE')
    const compositionDescription = navigation.getParam('compositionDescription', '')


    let sheet_ids = [];
    // to get all the sheet ids
    for (let i = 0; i < this.state.sheet_music.length; i++) {
        sheet_ids.push(this.state.sheet_music[i].getID());
    }


    onPressHandlerForInstrument = (item) => {
        console.log("ON PRESS HANDLER CLIKED\n\n\n\n\n")
        console.log("ITEM")
        console.log(item)
        console.log("\n\n\n\n\n\n")
        console.log(item.getFile())
        this.props.navigation.navigate('SelectMusicScreen', { refresh: this.refreshFunction, title: item.getTitle(), sheet_id: item.getID(), file: item.getFile() });
    }

    //     <TouchableOpacity
    //     onPress={(e) => {
    //         this.props.navigation.navigate('SelectMusicScreen', { title: item.getTitle(), sheet_id: item.getID(), file: item.getFile() })
    //     }}
    // >

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
                <DialogInput isDialogVisible={this.state.isAuthorDialogVisible}
                    title={"Edit Author"}
                    hintInput={"New Author"}
                    submitInput={(inputText) => {
                        // edit title
                        this.setAuthor(this.state.toEdit[1], inputText)
                        this.setState({ isAuthorDialogVisible: false, newAuthor: '' })
                    }}
                    closeDialog={() => { this.setState({ isAuthorDialogVisible: false, newAuthor: '' }) }}>
                </DialogInput>
                <DialogInput isDialogVisible={this.state.isTempoDialogVisible}
                    title={"Edit Tempo"}
                    hintInput={"Tempo Value"}
                    submitInput={(inputText) => {
                        // edit title
                        this.setTempo(this.state.toEdit[1], inputText)
                        this.setState({ isTempoDialogVisible: false, newTempo: 0 })
                    }}
                    closeDialog={() => { this.setState({ isTempoDialogVisible: false, newTempo: 0 }) }}>
                </DialogInput>
                <Text style={{ color: 'black', fontWeight: 'bold', fontSize: 40, width: "80%" }}> {compositionTitle} </Text>
                <View style={{ height: 100 }}>
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
                        <TouchableOpacity style={styles.neutralButton}
                            onPress={() => this.playComp(this.compID)}
                        >
                            <Icon
                                name="rightcircleo"
                                size={30}
                                color="white"
                            />
                        </TouchableOpacity>
                        {/* <TouchableOpacity style={styles.neutralButton} onPress={() => this.props.navigation.navigate('EditMusicScreen', {title: ""})}>
                            <Text style={styles.buttonText}>Edit</Text>
                        </TouchableOpacity> */}
                        <TouchableOpacity style={styles.minusButton} onPress={() => this.deleteComposition()}>
                            <Text style={styles.menuText}>-</Text>
                        </TouchableOpacity>
                    </View>
                </View>

                <Text style={{ color: 'black', }}>{compositionDescription}</Text>
                <ScrollView>
                    <FlatList
                        data={this.state.sheet_music}
                        extraData={this.state}
                        renderItem={({ item }) =>
                            <View style={styles.compositionContainer}>
                                <View style={styles.sheetItemContainer}>
                                    <TouchableOpacity
                                        style={styles.sheetItem}
                                        onPress={(e) => {

                                            this.props.navigation.navigate('EditMusicScreen', { title: item.getTitle(), file: item.getFile(), sheet_id: item.getID(), email: this.props.isRegistered, onBack: () => this.getInfo() })
                                        }}
                                        onLongPress={(e) => {
                                            this.setState({
                                                isDialogVisible: true,
                                                toEdit: [item.getTitle(), item.getID()], // getdescription actually gets the composition id
                                            })
                                        }}
                                    >
                                        <Text style={{ color: 'black', fontSize: 40 }}>{item.getTitle()}</Text>
                                    </TouchableOpacity>



                                    <TouchableOpacity style={styles.playButton}
                                        onPress={(e) => {
                                            this.playSong(item.getID())
                                        }}>
                                        <Icon
                                            name="caretright"
                                            size={15}
                                            color="white"
                                        />
                                    </TouchableOpacity>

                                </View>
                                <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'stretch' }}>
                                    <TouchableOpacity
                                        onPress={(e) => onPressHandlerForInstrument(item)}
                                    >
                                        <Text style={{ color: 'black', backgroundColor: 'white', borderRadius: 2, borderWidth: 3, borderColor: 'black', fontSize: 20 }}> {item.getInstrument() ? item.getInstrument() : "Piano"} </Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        style={{ flexGrow: 1 }}
                                        onPress={(e) => {
                                            this.setState({
                                                isAuthorDialogVisible: true,
                                                toEdit: [item.getTitle(), item.getID()]
                                            })
                                        }}
                                    >
                                        <Text style={{ color: 'black', backgroundColor: 'white', borderRadius: 2, borderWidth: 3, borderColor: 'black', fontSize: 20 }}> Author: {item.getAuthor()} </Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        onPress={(e) => {
                                            this.setState({
                                                isTempoDialogVisible: true,
                                                toEdit: [item.getTitle(), item.getID()]
                                            })
                                        }}
                                    >
                                        <Text style={{ color: 'black', backgroundColor: 'white', borderRadius: 2, borderWidth: 3, borderColor: 'black', fontSize: 20 }}> Tempo: {item.getTempo()} </Text>
                                    </TouchableOpacity>
                                </View>
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


                                    // <TouchableOpacity
                                    //     style={styles.sheetItem}
                                    //     onPress={(e) => {
                                    //         this.playSong(item.getID())
                                    //     }}>
                                    //     <Text style={{ color: 'black', fontSize: 40 }}> > </Text>
                                    // </TouchableOpacity>
