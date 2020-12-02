<template>
    <div>
      <div class="hero is-medium is-primary is-bold">
        <div class="hero-body">
          <div class="container">
            <h1 class="title">
              Repp
            </h1>
            <h2 class="subtitle">
              A tool for making sure your vote counts, after it's been counted
            </h2>
          </div>
        </div>
      </div>
      <div class="repp-process block">
        <b-steps :has-navigation="false" v-model="activeStep">
            <b-step-item label="Campaign" icon=""></b-step-item> 
            <b-step-item label="Election Day" icon=""></b-step-item>
            <b-step-item label="?" icon=""></b-step-item>
        </b-steps>

        <div class="repp-process-cols columns">
          <div v-for="(item, index) in steps" :key="item.name"
            class="column repp-process-step has-text-centered"
            v-bind:class="[{ 
              'repp-process-step-active': isActive(index),
              'repp-process-step-inactive': !isActive(index)
            }]"
          >
              <div
                v-bind:class="[{ 
                  'has-text-black-ter': isActive(index), 
                  'has-text-grey-light': !isActive(index)
                }]"
              >
                <p class="block lead">{{ item.lead }}</p>
                <p>{{ item.body }}</p>
              </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

export default {
  name: 'Home',
  components: {
  },
  methods: {
    init: async function() {
      for (let i = 0; i < this.steps.length - 1; i++) {
        await this.getStep(i) 
        this.activeStep = this.activeStep + 1
      }
    },
    isActive: function(step) {
      return step == this.activeStep
    },
    sleep: function(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    getStep: function(step) {
      return this.sleep(3500).then(() => this.steps[step])
    }
  },
  mounted() {
    this.init()
  },
  data() {
    return {
      steps: [
        {
          name: "campaign",
          lead: "First, they campaign",
          body: "Politicians campaign, and make promises to the people"
        },
        {
          name: "vote",
          lead: "Next, the people vote",
          body: "The people vote based on the candidate they think will fight for their interests"
        },
        {
          name: "question",
          lead: "Then what?",
          body: "How do you know that your representatives are voting with your interests in mind? Repp helps you find out!"
        }
      ],
      activeStep: 0,
    }
  },
}
</script>

<style scoped>
.repp-process-cols {
  padding-top: 1rem;
  padding-left: 2rem;
  padding-right: 2rem;
}

.repp-process-cols .lead {
  font-size: 1.5rem;
  font-weight: bold;
}

.repp-process-step-active {
  opacity: 1;
  transition-duration: 500ms;
}

.repp-process-step-inactive {
  opacity: 0.5;
}

.repp-process {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.repp-process .column {
  height: 8rem;
}

/* yanked this out of the inspector after overriding it in the browser */
.b-steps .steps.is-animated .step-item:not(:first-child)::before, .b-steps .steps.is-animated .step-item:only-child::before {
	transition: background 1s ease-out;
}
</style>
