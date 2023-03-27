import React from 'react'
import App from './App'

describe('<App />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<App/>)
  })

  it('displays dashboard title', () => {
    cy.mount(<App/>)
    cy.get('[id=dashboard-title]').should('have.text', 'Twitter Open Data Analyses and Visualisations: A closer look into sentiments during Malaysia\'s 15th General Election')
  })


  it('buttons show correct text', () => {
    cy.mount(<App/>)
    cy.get('[id=positive-btn]').should('have.text', 'Show Positive Only')
    cy.get('[id=negative-btn]').should('have.text', 'Show Negative Only')
    cy.get('[id=neutral-btn]').should('have.text', 'Show Neutral Only')
    cy.get('[id=all-sentiments-btn]').should('have.text', 'Show All Tweets By Date')
    cy.get('[id=reset-dashboard-btn]').should('have.text', 'Reset Dashboard')
  })


  it('labels show correct text', () => {
    cy.mount(<App/>)
    cy.get('[id=search-bar-label]').should('have.text', 'Enter your search word here: ')
    cy.get('[id=date-picker-text]').should('have.text', 'View Tweets by Date:')
  })

  it('search bar is visible', () => {
    cy.mount(<App/>)
    cy.get('[id=search-bar]').should('be.visible')
  })

  it('search input is empty', () => {
    cy.mount(<App/>)
    cy.get('[id=search-input-text]').should('be.empty')
  })

  it('date-picker is visible', () => {
    cy.mount(<App/>)
    cy.get('[id=date-picker]').should('be.visible')
  })

// case: first load, loading phase

  it('display texts are correct on first load, during loading', () => {
    cy.mount(<App/>)
    cy.get('[id=after-search-display-text]').should('have.text', 'Now showing dashboard for all tweets related to Malaysia\'s 15th General Election.')
    cy.get('[id=pie-chart-text]').should('have.text', 'Loading pie chart...')
    cy.get('[id=tweet-display-text]').should('have.text', 'Loading tweets...')
    cy.get('[id=line-chart-text]').should('have.text', 'Loading line chart...')
    cy.get('[id=top-ten-words]').should('have.text', 'Loading word cloud and top ten words display...')
  })


})

// cases to be implemented if time allows


// keyword only (yes and match, yes but no match, no)

// case 4: keyword (match) on submit changes
// case 4.1: after-search-display change
// case 4.2: pie chart text change
// case 4.3: pie chart change
// case 4.4: text display change
// case 4.5: tweet display change
// case 4.6: line chart text change
// case 4.7: line chart change
// case 4.8: top 10 words display change
// case 4.9: word cloud change

// case 5: keyword no match changes
// case 5.1: after-search-display change
// case 5.2: pie chart text change
// case 5.3: pie chart change
// case 5.4: text display change
// case 5.5: tweet display change
// case 5.6: line chart text change
// case 5.7: line chart change
// case 5.8: top 10 words display change
// case 5.9: word cloud change

// case 6: keyword empty changes
// case 6.1: after-search-display change
// case 6.2: pie chart text change
// case 6.3: pie chart change
// case 6.4: text display change
// case 6.5: tweet display change
// case 6.6: line chart text change
// case 6.7: line chart change
// case 6.8: top 10 words display change
// case 6.9: word cloud change

// sentiment only (pos, neg, neu, all)
// success case
// fail case

// date only (tweets available, tweets not available)
// success case
// fail case

// keyword and sentiment
// keyword yes, sentiment yes
// keyword yes, sentiment no
// assuming keyword no means sentiment must be no
// success case
// fail case

// keyword and date
// keyword yes, date yes
// keyword yes, date no
// assuming keyword no means date no

// sentiment and date
// sentiment yes, date yes
// sentiment yes, date no
// sentiment no, date yes
// sentiment no, date yes
// sentiment no, date no

// keyword and sentiment and date
// keyword yes, sentiment yes, date yes
// keyword yes, sentiment yes, date no
// keyword yes, sentiment no, date no
// keyword no - everything else no

// reset button

// on refresh