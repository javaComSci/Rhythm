import React from 'react';
import { connect } from 'react-redux';
import { StyleSheet, View, Text, TouchableOpacity, Image, ScrollView } from 'react-native';
import { Table, TableWrapper, Row, Rows, Col, Cols, Cell } from 'react-native-table-component';

class SelectMusicScreen extends React.Component {

	constructor(props){
		super(props);

		this.state = {
			tableData: [
				['Piano', 'Harp'],
				['Violin', 'Flute'],
				['Tuba', 'Guitar'],
				['Cello', 'Bass'],
				['Trombone', 'Viola']
			],
			sheet_id: this.props.navigation.getParam('sheet_id'),
		};

	}

	static navigationOptions = {
    	title: 'Welcome', header: null
  	};

	chooseInstrument(instrument) {
		console.log("YOU CHOSE" + instrument + "  with sheet id as " + this.state.sheet_id + " " + this.props.testing);

		fetch('http://18.237.79.152:5000/selectInstrument', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                	'instrument': instrument,
                	'sheet_id': this.state.sheet_id,
                }),
            }).then((res) => {
                this.props.navigation.navigate('ViewCompScreen')
            }).catch((res) => {
                console.log("err", res)
            });
	}

	getImage(instrument){
		switch(instrument){
			case 'Piano': return (<Image style={styles.img} source={require('../assets/piano.png')} />);
			case 'Harp': return (<Image style={styles.img} source={require('../assets/harp.png')} />);
			case 'Violin': return (<Image style={styles.img} source={require('../assets/violin.png')} />);
			case 'Flute': return (<Image style={styles.img} source={require('../assets/flute.png')} />);
			case 'Drums': return (<Image style={styles.img} source={require('../assets/drums.png')} />);
			case 'Guitar': return (<Image style={styles.img} source={require('../assets/guitar.png')} />);
			case 'Cello': return (<Image style={styles.img} source={require('../assets/cello.png')} />);
			case 'Bass': return (<Image style={styles.img} source={require('../assets/bass.png')} />);
			case 'Tuba': return (<Image style={styles.img} source={require('../assets/tuba.png')} />);
			case 'Viola': return (<Image style={styles.img} source={require('../assets/viola.png')} />);
		}
	}

	instrumentButton(instrument) {
		return (
			 <TouchableOpacity onPress={() => this.chooseInstrument(instrument)}>
        		<View style={styles.btn}>
          			<Text style={styles.btnText}>{instrument}</Text>
			        {this.getImage(instrument)}
        		</View>
      		</TouchableOpacity>
		);

	}

	createButtonElements() {
		console.log('props',this.state.tableData);
		return (
          
            this.state.tableData.map((rowData, index) => (
              <TableWrapper key={index} style={styles.row}>
                {
                  rowData.map((cellData, cellIndex) => {
                    console.log("celldata" + cellData + " " +cellIndex);
                    return <Cell key={cellIndex} data={this.instrumentButton(cellData)} textStyle={styles.text}/>
                  })
                }
              </TableWrapper>
            ))
		);
	}

    render() {
        return (
	        <View styles={styles.container}>
	        	<Text style={{fontSize: 30, marginTop: '5%', fontWeight: 'bold'}}> Choose Instrument </Text>
	        	<Table style={{height:'100%', marginTop: '5%'}} borderStyle={{borderWidth: 3, borderRadius: 5, borderColor: '#9fa1a5'}}>
	        		{this.createButtonElements()}
	        	</Table>
	        </View>
        )
    }
}


const styles = StyleSheet.create({
  container: { flex: 1, padding: 100, paddingTop: 20, backgroundColor: '#000', height: '100%' },
  text: { margin: 6 },
  row: { flexDirection: 'row'},
  btn: { width: 200, height: 150, backgroundColor: '#e8eaef', borderRadius: 2, justifyContent: 'center', alignItems: 'center' },
  btnText: { textAlign: 'center', color: '#000', fontSize: 20, paddingBottom: '5%' },
  img: {width: '60%', height: '60%', backgroundColor: 'transparent', resizeMode: 'contain'},
});


export default SelectMusicScreen;