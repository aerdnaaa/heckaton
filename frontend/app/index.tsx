import React from 'react';
import { Text, View, StyleSheet, TextInput, Button, ActivityIndicator } from "react-native";
import { MdAccessTime } from "react-icons/md";
import { createServer } from "miragejs";
import IngredientComponent from '@/components/ingredient/IngredientComponent';
import InstructionComponent from '@/components/instruction/InstructionComponent';

createServer({
  routes() {
    this.post("/submit", () => {
      return {
        prep_time: 20,
        cooking_time: 20,
        total_time: 40,
        instructions: ["1.Preheat oven to 350°F (175°C) and line a muffin tin with liners", "2.In a large bowl, mash the bananas until smooth", "3.Stir in melted butter, sugar, egg, and vanilla extract until well combined", "4.In another bowl, whisk together flour, baking soda, and salt"],
        ingredients: [{ item: "hi", qty: 2, unit: "hi" }, { item: "hi", qty: 4, unit: "h2i" }],
      }
    })
  },
})

const Index = () => {
  const [url, onChangeUrl] = React.useState('');
  const [displaySearchBar, setDisplaySearchBar] = React.useState(true);
  const [isLoading, setLoading] = React.useState(false);
  const [recipe, setRecipe] = React.useState(false);
  const [prepTime, setPrepTime] = React.useState(NaN);
  const [cookingTime, setCookingTime] = React.useState(NaN);
  const [totalTime, setTotalTime] = React.useState(NaN);
  const [ingredients, setIngredients] = React.useState([]);
  const [instructions, setInstructions] = React.useState([]);
  const getRecipe = () => {
    setLoading(true);
    return fetch('https://localhost:8081/submit', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'url': url,
      }),
    })
      .then(response => response.json())
      .then(json => {
        setRecipe(true);
        setPrepTime(json.prep_time);
        setCookingTime(json.cooking_time);
        setTotalTime(json.total_time);
        setIngredients(json.ingredients);
        setInstructions(json.instructions);
        onChangeUrl('');
        setDisplaySearchBar(false);
        setLoading(false);
      });
  };
  const getAnotherRecipe = () => {
    setDisplaySearchBar(true);
    setRecipe(false);
  }
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: '#fdfbd4',
      }}
    >
      {displaySearchBar ?
        <View style={styles.head}>
          <Text>Welcome To !!</Text>
          <TextInput
            onChangeText={onChangeUrl}
            value={url}
            placeholder='Enter URL of food video...'
            style={styles.input}
          />
          <Button
            onPress={getRecipe}
            title='Submit'
            color='#f56f42'
          />
        </View>
        : <Button
          onPress={getAnotherRecipe}
          title='Try Another Recipe'
          color='#f56f42'
        />
      }

      {
        isLoading ?
          <ActivityIndicator size="large" color="#f56f42" />
          : <View></View>
      }

      {
        recipe ?
          <View style={styles.recipeContainer}>
            <View style={styles.timingHeaders}>
              <View style={styles.timingDiv}>
                <Text style={styles.smallFont}>
                  {prepTime} min
                </Text>
                <Text style={styles.smallFont}>Preparation</Text>
              </View>
              <View style={styles.timingDiv}>
                <MdAccessTime style={styles.mediumFont} />
                <Text style={styles.mediumFont}>
                  {totalTime} min
                </Text>
                <Text style={styles.mediumFont}>Total</Text>
              </View>
              <View style={styles.timingDiv}>
                <Text style={styles.smallFont}>
                  {cookingTime} min
                </Text>
                <Text style={styles.smallFont}>Cooking</Text>
              </View>
            </View>
            <View style={styles.details}>
              <IngredientComponent ingredients={ingredients} />
              <InstructionComponent instructions={instructions} />
            </View>
          </View>
          : <View></View>
      }
    </View >
  );
}

const styles = StyleSheet.create({
  head: {
    display: 'flex',
    alignItems: 'center',
    width: '90%',
    paddingBottom: 20,
  },
  input: {
    height: 40,
    margin: 12,
    width: '100%',
    borderWidth: 1,
    padding: 10,
  },
  recipeContainer: {
    paddingTop: 20,
    width: '90%'
  },
  timingHeaders: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: "space-evenly",
    alignItems: "center",
    width: '100%',
  },
  timingDiv: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '20%',
  },
  smallFont: {
    fontSize: 24,
  },
  mediumFont: {
    fontSize: 30,
    fontWeight: 'bold'
  },
  details: {
    paddingTop: 20,
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-around',
  }
});

export default Index;