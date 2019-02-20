import React from 'react';
import { FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';

var styles = require('../style');
/*
todo: get compositions from database
*/

/*
Composition class
*/
class Composition {
    constructor(title, description, id) {
        this.title = title;
        this.description = description;
        this.key = id.toString(); // must be stored as string for FlatList
        this.sheetMusic = [];
    }

    getTitle = function () {
        return this.title;
    }
}

export default class CompositionScreen extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            "compositions": []
        }
    }
    static navigationOptions = {
        title: 'Welcome', header: null
    };

    componentWillMount() {
        const that = this; // a reference to the previous value of "this" is required as there is a context change going into the promise of the fetch
        fetch('http://18.237.79.152:5000/getInfo', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'table': 'composition',
                'id': 1
            }),
        }).then((res) => {
            res.text().then(function (res) {
                var dummyList = [] // temp list to hold compositions before being added to state
                JSON.parse(res).forEach(element => {
                    dummyList.push(new Composition(element[1], element[2], element[0]));
                });
                that.setState({ "compositions": dummyList })
            })
                .catch((err) => {
                    console.log("err", err)
                })
        }).catch((res) => {
            console.log("err", res)
        });
    }

    componentDidMount() {
    }

    render() {
        return (
            <View style={styles.container}>
                <View style={styles}>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> COMPOSITIONS </Text>
                    <View style={styles.lineBreak} />
                </View>
                <ScrollView>
                    <FlatList
                        data={this.state.compositions}
                        extraData={this.state}
                        renderItem={({ item }) =>
                            <View style={styles.compositionContainer}>
                                <TouchableOpacity style={styles.compositionItem}>
                                    <Text style={{ color: '#f19393', fontSize: 40 }}>{item.getTitle()}</Text>
                                </TouchableOpacity>
                                <View style={styles.lineBreak} />
                            </View>}
                    />
                </ScrollView>
                <View style={styles.footer}>
                    <TouchableOpacity onPress={() => this.props.navigation.navigate('Home')} style={styles.navButton}>
                        <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Home </Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    }
};
