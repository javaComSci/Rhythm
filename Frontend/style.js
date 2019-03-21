'use strict';

var React = require('react-native');

var {
    StyleSheet,
} = React;

module.exports = StyleSheet.create({
    header: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    menuButton: {
        marginTop: 10,
        paddingTop: 20,
        paddingBottom: 20,
        width: "33%",
        backgroundColor: 'black',
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#fff'
    },
    headerWithMenu: {
        flex: 1,
        flexDirection: 'row',
    },
    headerText: {
        fontSize: 20,
        margin: 10,
        fontWeight: "bold"
    },
    iconText: {
        fontSize: 40,
        fontWeight: "bold"
    },
    menuContent: {
        color: "#000",
        fontWeight: "bold",
        padding: 2,
        fontSize: 20
    },
    buttonText: {
        textAlign: 'center',
        color: 'white'
    },
    container: {
        flex: 1,
        marginTop: 20,
        //backgroundColor: '#ffeceb',
    },
    editContainer: {
        flex: 1,
        marginTop: 20,
        backgroundColor: '#ffffff',
    },
    textHolder: {
        height: 200,
        alignItems: 'center'
    },
    footer: {
        height: 100,
        //backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center'
    },
    menuText: {
        color: 'white',
        fontSize: 40
    },
    navButton: {
        height: 75,
        position: 'absolute', top: 0, bottom: 0, left: 0, right: 0,
        textAlign: 'center',
        marginTop: 10,
        marginBottom: 30,
        paddingTop: 15,
        marginLeft: 100,
        marginRight: -30,
        borderRadius: 10,
        backgroundColor: 'black',
        borderColor: 'white',
        borderWidth: 1,
    },
    openButton: {
        height: 75,
        width: "70%",
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 10,
        marginBottom: 30,
        paddingTop: 15,
        paddingBottom: 50,
        borderRadius: 10,
        backgroundColor: 'transparent',
        borderColor: 'white',
        borderWidth: 1,
    },
    operatorContainer: {
        flex: 1,
        flexDirection: 'row',
        maxHeight: 75,
        flexWrap: 'nowrap',
        justifyContent: 'space-between',
    },
    addButton: {
        height: 75,
        width: 150,
        alignItems: 'center',
        justifyContent: 'center',
        marginLeft: -15,
        borderRadius: 10,
        backgroundColor: 'transparent',
        borderColor: 'white',
        borderWidth: 1,
    },
    minusButton: {
        height: 75,
        width: 150,
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: -15,
        borderRadius: 10,
        backgroundColor: 'transparent',
        borderColor: 'white',
        borderWidth: 1,
    },
    neutralButton: {
        height: 75,
        width: 75,
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 10,
        backgroundColor: 'transparent',
        borderColor: 'white',
        borderWidth: 1,
    },
    lineBreak: {
        borderBottomColor: 'black',
        borderBottomWidth: 1,
    },
    compositionContainer: {
        margin: 40
    },
    compositionItem: {
        height: 50,
    },
    inputContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
});
