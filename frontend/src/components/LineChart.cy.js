import React from 'react'
import LineChart from './LineChart'

describe('<LineChart />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<LineChart />)
  })
})