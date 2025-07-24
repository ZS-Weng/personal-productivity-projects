import sveltePreprocess from 'svelte-preprocess';

export default {
  preprocess: sveltePreprocess(),
  compilerOptions: {
    // enable run-time checks when not in production
    dev: !process.env.NODE_ENV === 'production',
  },
};