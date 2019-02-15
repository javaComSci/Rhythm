import React from 'react';
import { FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';

var styles = require('../style');

export default class CompositionScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
                <View style={styles}>
                    <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> COMPOSITIONS </Text>
                    <View style={styles.lineBreak} />
                </View>
                <ScrollView>
                    <FlatList
                        data={[
                            // to be filled with data from Async local storage
                            { key: "composition 1" },
                            { key: "composition 2" }
                        ]}
                        renderItem={({ item }) =>
                            <View style={styles.compositionContainer}>
                                <TouchableOpacity style={styles.compositionItem}>
                                    <Text style={{ color: '#f19393', fontSize: 40 }}>{item.key}</Text>
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
