import React from 'react'
import PieChart from './PieChart'

describe('<PieChart />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-react
    cy.mount(<PieChart />)
  })
})