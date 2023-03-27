import React from 'react'
import TweetDisplay from './TweetDisplay'

describe('<TweetDisplay />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<TweetDisplay />)
  })
})