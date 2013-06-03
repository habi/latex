T=0.3;
A=0.3;
t=0:0.01:4*T;
n1=length(t);
N=100;
s=0;

signal=0;
for i=1:n1
s=0;
for n=1:N
s=s+A*4/(pi*(2*n-1))*sin(2*pi*(2*n-1)/T*t(i));
end
signal(i)=s;
end
plot(t,signal);

matlab2tikz()