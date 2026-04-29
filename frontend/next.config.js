/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@radix-ui'],
  env: {
    CUSTOM_KEY: 'value',
  },
};

module.exports = nextConfig;
