import React from 'react';
import { View, Image, StyleSheet, TouchableOpacity, Text, Dimensions } from 'react-native';
import { Feather } from '@expo/vector-icons';

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

export default function ResultScreen({ route, navigation}) {
  const { photo } = route.params;

  return (
    <View style={styles.container}>
      <Image source={{ uri: photo }} style={styles.image} />
      <View style={styles.overlay}>
        <View style={styles.analyze}>
          <View style={styles.analyzeLeft}>
            <Text style={styles.content}>• Genel Kategori:</Text>
            <Text style={styles.content}>• Kategori Sayısı:</Text>
            <Text style={styles.content}>• Kategori Uyumu:</Text>
            <Text style={styles.content}>• Aykırı Ürün:</Text>
          </View>
          <View style={styles.analyzeRight}>
            <Text style={styles.title}>Öneriler</Text>
            <Text style={styles.listItem}>• </Text>
            <Text style={styles.listItem}>• </Text>
            <Text style={styles.listItem}>• </Text>
          </View>
        </View>
        <View style={styles.refresh}>
        <TouchableOpacity onPress={() => navigation.navigate('Camera', { key: Date.now() })}>
            <Feather name="refresh-ccw" size={24} color="#3CB371" />
        </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'black',
  },
  image: {
    position: 'absolute',
    width: screenWidth,
    height: screenHeight,
  },
  overlay: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    marginBottom: 100,
  },
  analyze: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: screenWidth - 60,
  },
  analyzeRight: {
    width:screenWidth/2,
    
  },
  analyzeLeft: {
    width:screenWidth/2,
    
  },
  refresh: {
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.8,
    shadowRadius: 3,
    elevation: 5, 
  },
  title: {
    fontWeight: 'bold',
    textDecorationLine: 'underline',
    fontSize: 24,
    color: '#3CB371', 
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 10
  },
  content: {
    fontWeight: '600',
    color: '#CD5C5C', 
    fontSize: 20,
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 10
  },
  listItem: {
    fontWeight: '600',
    color: '#F5F5DC', 
    fontSize: 18,
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: -1, height: 1 },
    textShadowRadius: 10
  },
});
