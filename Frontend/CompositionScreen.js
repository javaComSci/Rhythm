import React from 'react';
import { FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';


export default class ProfileScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
                <View>
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
                                    <Text style={{ fontSize: 40 }}>{item.key}</Text>
                                </TouchableOpacity>
                                <View style={styles.lineBreak} />
                            </View>}
                    />
                </ScrollView>
                <View>
                    <Button
                        title="Back"
                        onPress={() => this.props.navigation.navigate('Home')}
                    />
                </View>
            </View>
        );
    }
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center',
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
    header: {
        height: 56 // standard for iOS devices
    }
});